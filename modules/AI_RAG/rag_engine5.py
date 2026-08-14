import os
import sys
import json
import uuid
from dotenv import load_dotenv
from ddgs import DDGS
from openai import OpenAI
import chromadb
import sqlite3

# schema.py에서 정의한 데이터 클래스들 불러오기
current_dir = os.path.dirname(os.path.abspath(__file__))
# AI_RAG 폴더의 상위(modules)와 최상위(QR-Checker) 경로를 모두 추가
sys.path.append(os.path.abspath(os.path.join(current_dir, "../")))
sys.path.append(os.path.abspath(os.path.join(current_dir, "../../")))

############################ 원본 ############################
# # ✅ 팀원이 만든 ML 탐지기 및 피처 추출 함수 가져오기 완성
# from schema import DetectionResult, AnalysisResult, FeatureVector
# from ml_detector import MaliciousURLDetector
# from url_to_feature import extract_features  
#############################################################

from ..schema import DetectionResult, AnalysisResult, FeatureVector
from ..ml_detector import MaliciousURLDetector
from ..url_to_feature import extract_features

load_dotenv()

# ---------------------------------------------------------
# [상태 관리용 인메모리 딕셔너리] 
# ---------------------------------------------------------
sessions = {}

class RAGEngine:
    def __init__(self):
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY가 설정되지 않았습니다.")
        
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # 1. Chroma DB 클라이언트 및 컬렉션 연결
        CHROMA_DIR = os.path.join(current_dir, "docs", "chroma_db")
        COLLECTION_NAME = "qr_quishing_kb"
        
        self.chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
        self.collection = self.chroma_client.get_or_create_collection(name=COLLECTION_NAME)
        print(f"Chroma DB 연결 완료 (총 {self.collection.count()}개 문서 적재됨)")

        # 2. 사용자 DB (SQLite) 연동 세팅
        self.db_path = os.path.join(current_dir, "data", "user_malicious.db")
        self._init_db()

        # 3. 웹 검색 제한(Search Budget & Hash Guard) 세팅
        self.search_budget = 3       
        self.search_count = 0        
        self.searched_queries = set() 

        # 4. ML 탐지기 객체 초기화
        try:
            self.ml_detector = MaliciousURLDetector('lgbm')
        except Exception as e:
            print(f"[ML_Detector] 초기화 실패: {e}")
            self.ml_detector = None

    # ---------------------------------------------------------
    # [사용자 DB 연동 기능]
    # ---------------------------------------------------------
    def _init_db(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS malicious_urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def check_external_database(self, url: str) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM malicious_urls WHERE url = ?", (url,))
        result = cursor.fetchone()
        conn.close()
        
        is_bad = result is not None
        print(f"[DB Search] {url} 악성 여부: {is_bad}")
        return is_bad

    def register_malicious_url(self, url: str):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO malicious_urls (url) VALUES (?)", (url,))
            conn.commit()
            conn.close()
            print(f"[DB Register] {url} 악성 URL DB 등록 완료!")
        except sqlite3.IntegrityError:
            print(f"[DB Register] {url} 이미 DB에 등록된 URL입니다.")

    # ---------------------------------------------------------
    # [웹 검색 로직]
    # ---------------------------------------------------------
    def perform_web_search(self, query: str) -> str:
        if query in self.searched_queries:
            return "System Action: 이미 검색했던 내용이야. 기존 정보를 바탕으로 답변해 줘."

        if self.search_count >= self.search_budget:
            return "System Action: 검색 한도를 초과했어. 지금까지 찾은 정보만으로 최종 판단을 내려 줘."

        self.searched_queries.add(query)
        self.search_count += 1
        print(f"[Web Search] '{query}' 검색 중... ({self.search_count}/{self.search_budget})")
        
        try:
            with DDGS() as ddgs:
                results = ddgs.text(query, max_results=3)
                if not results:
                    return f"'{query}'에 대한 검색 결과가 없습니다."
                
                search_text = "다음은 웹 검색 결과입니다:\n"
                for i, res in enumerate(results, 1):
                    search_text += f"{i}. [제목]: {res['title']}\n   [내용]: {res['body']}\n   [링크]: {res['href']}\n\n"
                
                return search_text
        except Exception as e:
            print(f"[오류] 웹 검색 중 에러 발생: {e}")
            return "System Action: 일시적인 검색 엔진 오류로 검색을 수행할 수 없어. 기존 내부 문서를 활용해 줘."

    # ---------------------------------------------------------
    # [유사도 검색]
    # ---------------------------------------------------------
    def _retrieve_relevant_docs(self, query_text : str, n_results: int = 3) -> str:
        resp = self.client.embeddings.create(
            model = "text-embedding-3-small",
            input=[query_text]
        )
        query_embedding = resp.data[0].embedding

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]

        combined_text = ""
        for doc, meta in zip(documents, metadatas):
            source = meta.get("source", "보안 지침")
            combined_text += f"\n\n--- [출처: {source} ---\n {doc}]"

        return combined_text

    # ---------------------------------------------------------
    # 1. 초기 스캔 결과 처리
    # ---------------------------------------------------------
    def init_scan(self, url: str, detection_result: DetectionResult) -> dict:
        is_ml_bad = detection_result.is_malicious
        is_db_bad = self.check_external_database(url)
        
        is_malicious_final = is_ml_bad or is_db_bad
        
        if not is_malicious_final:
            return {
                "status": "completed",
                "result": AnalysisResult(reason="안전한 URL로 확인되었습니다.", countermeasures=["특이사항 없음"])
            }

        if not is_db_bad:
            self.register_malicious_url(url)
            
        session_id = str(uuid.uuid4())
        
        self.search_count = 0
        self.searched_queries.clear()
        
        sessions[session_id] = {
            "url": url,
            "state": "ASKED_ACCESS", 
            "confidence": detection_result.confidence_score
        }

        return {
            "status": "chat_required",
            "session_id": session_id,
            "message": f"위험한 QR로 판정되었습니다! ({detection_result.confidence_score*100:.1f}%)\n해당 링크에 접속하셨나요? (예/아니오)"
        }

    # ---------------------------------------------------------
    # 2. 대화 핑퐁 처리 
    # ---------------------------------------------------------
    def chat(self, session_id: str, user_message: str) -> dict:
        if session_id not in sessions:
            return {"status": "error", "message": "유효하지 않거나 만료된 세션입니다."}

        session_data = sessions[session_id]
        current_state = session_data["state"]

        if current_state == "ASKED_ACCESS":
            if "아니" in user_message or "안" in user_message:
                return self._generate_final_guide(
                    session_id, 
                    "사용자가 악성 링크에 접속하지 않았습니다. 즉시 삭제를 권장하는 예방 수칙 위주로 가이드를 주세요."
                )
            else:
                session_data["state"] = "ASKED_ACTION"
                return {
                    "status": "chat_required",
                    "session_id": session_id,
                    "message": "어떤 페이지였거나, 어떤 행동을 하셨나요?\n1. 로그인/비밀번호 입력\n2. 파일(.apk, .exe 등) 다운로드\n3. 단순 접속만 한 뒤 닫음"
                }

        elif current_state == "ASKED_ACTION":
            prompt = f"사용자가 링크에 접속했으며, 다음 행동을 했습니다: {user_message}\n이에 맞는 강력한 사후 대응 지침을 주세요."
            return self._generate_final_guide(session_id, prompt)

        return {"status": "error", "message": "알 수 없는 상태입니다."}

    # ---------------------------------------------------------
    # 3. 내부용 헬퍼: 최종 가이드(RAG) 생성 후 AnalysisResult 반환
    # ---------------------------------------------------------
    def _generate_final_guide(self, session_id: str, context_prompt: str) -> dict:
        system_instructions = (
            "너는 전문적인 보안 컨설턴트야. 제공된 [보안 지침 문서]와 필요시 [웹 검색 결과], "
            "그리고 [머신러닝 모델 예측 결과]를 종합해서 사용자의 상황에 맞는 판단 사유와 대응 지침을 작성해 줘. "
            "반드시 아래 JSON 형식으로만 정확하게 답변해.\n"
            "{\n"
            "  \"reason\": \"위험/안전 판단 상세 사유\",\n"
            "  \"countermeasures\": [\"대응 지침 1\", \"대응 지침 2\"],\n"
            "  \"source\": \"참고한 핵심 출처\"\n"
            "}"
        )
        
        retrieved_context = self._retrieve_relevant_docs(context_prompt, n_results=3)

        user_input =(
            f"상황: {context_prompt}\n\n"
            f"[보안 지침 문서]\n{retrieved_context}"
        )

        messages = [
            {"role": "system", "content": system_instructions},
            {"role": "user", "content": user_input}
        ]

        tools = [
            {
                "type": "function",
                "function": {
                    "name": "perform_web_search",
                    "description": "최신 악성 URL 및 피싱 수법에 대한 추가 정보가 필요할 때 웹 검색을 수행합니다.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "검색할 키워드"}
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "predict_malicious_url",
                    "description": "사용자가 접속한 URL을 자체 머신러닝 모델에 입력하여 악성 여부와 확률을 예측합니다.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "url": {"type": "string", "description": "검사할 대상 URL"}
                        },
                        "required": ["url"]
                    }
                }
            }
        ]

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                tools=tools,
                tool_choice="auto" 
            )

            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls

            if tool_calls:
                messages.append(response_message) 

                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    if function_name == "perform_web_search":
                        function_response = self.perform_web_search(
                            query=function_args.get("query")
                        )
                        
                    elif function_name == "predict_malicious_url":
                        target_url = function_args.get("url")
                        if self.ml_detector:
                            try:
                                # ✅ 더미 코드 삭제 완료: 실제 피처 추출 및 예측 수행
                                features = extract_features(target_url) 
                                ml_result = self.ml_detector.predict(features)
                                
                                status = "악성" if ml_result.is_malicious else "정상"
                                score = ml_result.confidence_score * 100
                                function_response = f"[시스템] 머신러닝 분석 완료. 대상 URL '{target_url}'은(는) '{status}'으로 분류됨. (위험 확률: {score:.1f}%)"
                            except Exception as e:
                                function_response = f"ML 분석 중 에러 발생: {e}"
                        else:
                            function_response = "ML 모델이 로드되지 않아 분석할 수 없습니다."

                    messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    })

                second_response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=messages,
                )
                assistant_response = second_response.choices[0].message.content
            else:
                assistant_response = response_message.content

            clean_json_str = assistant_response.replace("```json", "").replace("```", "").strip()
            parsed_data = json.loads(clean_json_str)

            if session_id in sessions:
                del sessions[session_id]

            reason_text = parsed_data.get("reason", "분석 사유를 불러오지 못했습니다.")
            source_text = parsed_data.get("source", "")
            if source_text:
                reason_text += f" (출처: {source_text})"

            analysis_result = AnalysisResult(
                reason=reason_text,
                countermeasures=parsed_data.get("countermeasures", ["대응 지침 없음"])
            )

            return {
                "status": "completed",
                "result": analysis_result
            }

        except Exception as e:
            print(f"[오류] RAG 생성 중 에러 발생: {e}")
            return {"status": "error", "message": "서버 통신 오류"}

# ---------------------------------------------------------
# 단독 테스트 실행 코드
# ---------------------------------------------------------
if __name__ == "__main__":
    engine = RAGEngine()
    test_url = "http://g00gle-login.com:8080/verify"
    mock_detection = DetectionResult(is_malicious=True, confidence_score=0.98)
    
    print("\n--- 1. 큐알 스캔 발생 (악성) ---")
    response1 = engine.init_scan(url=test_url, detection_result=mock_detection)
    print("앱으로 보낼 응답:", response1)
    
    if response1["status"] == "chat_required":
        session_id = response1["session_id"]
        
        print("\n--- 2. 사용자가 '네 접속했어요' 라고 대답함 ---")
        response2 = engine.chat(session_id=session_id, user_message="네 접속했어요")
        print("앱으로 보낼 응답:", response2)
        
        if response2["status"] == "chat_required":
            print("\n--- 3. 사용자가 '1번 로그인했어요' 라고 대답함 ---")
            response3 = engine.chat(session_id=session_id, user_message="1. 로그인/비밀번호 입력")
            
            print("\n--- [최종 도출된 Analysis Result] ---")
            if response3["status"] == "completed":
                final_analysis: AnalysisResult = response3["result"]
                print(f"Reason: {final_analysis.reason}")
                print(f"Countermeasures: {final_analysis.countermeasures}")