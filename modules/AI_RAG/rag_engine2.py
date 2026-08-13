import os
import sys
import json
import uuid
from dotenv import load_dotenv
from openai import OpenAI
from openai import APIError, APIConnectionError, RateLimitError

# schema.py에서 정의한 데이터 클래스들 불러오기
current_dir = os.path.dirname(os.path.abspath(__file__))
# AI_RAG 폴더의 상위(modules)와 최상위(QR-Checker) 경로를 모두 추가해 줘
sys.path.append(os.path.abspath(os.path.join(current_dir, "../")))
sys.path.append(os.path.abspath(os.path.join(current_dir, "../../")))
from schema import DetectionResult, AnalysisResult

load_dotenv()

# ---------------------------------------------------------
# [상태 관리용 인메모리 딕셔너리] 
# 실제 서버 배포 시에는 Redis나 DB로 교체
# ---------------------------------------------------------
sessions = {}

class RAGEngine:
    def __init__(self):
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY가 설정되지 않았습니다.")
        
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # 상대경로가 안 먹힐 경우
        current_dir = os.path.dirname(os.path.abspath(__file__))
        docs_path = os.path.join(current_dir, "docs")
        # 초기화할 때 마크다운 문서들을 미리 읽어서 메모리에 올려둠
        # 프로젝트 폴더 안에 'docs'라는 폴더를 만들고 거기에 md 파일들을 넣어둠
        self.knowledge_base = self._load_local_documents(docs_path)

    def _load_local_documents(self, docs_dir: str) -> str:
        """기능: 지정된 폴더의 모든 .md 파일을 읽어서 하나의 문자열로 병합"""
        combined_text = ""
        if not os.path.exists(docs_dir):
            print(f"[경고] '{docs_dir}' 폴더가 없습니다. 문서를 불러오지 못했습니다.")
            return combined_text
            
        for filename in os.listdir(docs_dir):
            if filename.endswith(".md"):
                filepath = os.path.join(docs_dir, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        combined_text += f"\n\n--- [출처: {filename}] ---\n"
                        combined_text += f.read()
                except Exception as e:
                    print(f"[오류] {filename} 읽기 실패: {e}")
                    
        print(f"[시스템] 총 {len(combined_text)}자의 로컬 지식 베이스 로드 완료.")
        return combined_text

    def check_external_database(self, url: str) -> bool:
        """기능: 외부 DB(악성 URL 리스트) 조회"""
        print(f"[DB Search] {url} 외부 DB 조회 중...")
        return False

    def register_malicious_url(self, url: str):
        """기능: 악성 URL 사용자 DB 등록"""
        print(f"[DB Register] {url} 악성 URL DB 등록 완료!")

    # ---------------------------------------------------------
    # 1. 초기 스캔 결과 처리 (QR 찍고 난 직후)
    # ---------------------------------------------------------
    def init_scan(self, url: str, detection_result: DetectionResult) -> dict:
        is_bad_in_db = self.check_external_database(url)
        is_malicious_final = detection_result.is_malicious or is_bad_in_db
        
        if not is_malicious_final:
            return {
                "status": "completed",
                "result": AnalysisResult(reason="안전한 URL로 확인되었습니다.", countermeasures=["특이사항 없음"])
            }

        self.register_malicious_url(url)
        session_id = str(uuid.uuid4())
        
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
            "너는 전문적인 보안 컨설턴트야. 제공된 [보안 지침 문서]를 반드시 참고해서 사용자의 상황에 맞는 판단 사유와 대응 지침을 작성해 줘. "
            "가장 관련 깊은 문서의 이름을 출처로 명시해야 해. "
            "반드시 마크다운이나 추가 설명 없이 아래 JSON 형식으로만 정확하게 답변해.\n"
            "{\n"
            "  \"reason\": \"위험/안전 판단 상세 사유\",\n"
            "  \"countermeasures\": [\"대응 지침 1\", \"대응 지침 2\"],\n"
            "  \"source\": \"참고한 핵심 문서 출처 (예: kisa_filtered.md)\"\n"
            "}"
        )
        
        # [수정] 미리 읽어둔 md 파일 내용(knowledge_base)을 프롬프트에 통째로 주입!
        user_input = (
            f"상황: {context_prompt}\n\n"
            f"[보안 지침 문서]\n{self.knowledge_base}"
        )

        try:
            response = self.client.responses.create(
                model="gpt-5.6", 
                instructions=system_instructions,
                input=user_input,
            )

            assistant_response = response.output_text
            clean_json_str = assistant_response.replace("```json", "").replace("```", "").strip()
            parsed_data = json.loads(clean_json_str)

            if session_id in sessions:
                del sessions[session_id]

            # [수정] schema.py에 source가 아직 없다면, reason 문자열에 붙여서 임시로 에러 방지
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
# 단독 테스트 실행 코드 (테스트용)
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