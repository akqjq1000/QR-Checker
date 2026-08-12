import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from openai import APIError, APIConnectionError, RateLimitError

# ---------------------------------------------------------
# 1. 공통 스키마 파일에서 약속된 데이터 형식 불러오기
# ---------------------------------------------------------
from schema import DetectionResult, AnalysisResult

# .env 파일에서 환경 변수 불러오기 (루트 경로 기준)
load_dotenv()

# ---------------------------------------------------------
# 2. AI·RAG 엔진 메인 클래스
# ---------------------------------------------------------
class RAGEngine:
    def __init__(self):
        # OpenAI 클라이언트 및 Assistant ID 초기화
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY가 설정되지 않았습니다.")
        if not os.getenv("OPENAI_ASSISTANT_ID"):
            raise ValueError("OPENAI_ASSISTANT_ID가 설정되지 않았습니다.")
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.assistant_id = os.getenv("OPENAI_ASSISTANT_ID")

    def check_external_database(self, url: str) -> bool:
        """기능 2: 외부 DB(악성 URL 리스트) 조회"""
        print(f"[DB Search] {url} 외부 DB 조회 중...")
        # TODO: 실제 외부 데이터베이스 조회 로직 추가
        return False

## 사용자가 등록하는 DB가 필요할까요????

    def register_malicious_url(self, url: str):
        """기능 4: 악성 URL 사용자 DB 등록"""
        print(f"[DB Register] {url} 악성 URL DB 등록 완료!")
        # TODO: 판단된 악성 URL을 우리 데이터베이스에 저장하는 로직 추가

    def generate_rag_response(self, url: str, is_malicious_final: bool, confidence_score: float) -> AnalysisResult:
        """기능 1: OpenAI Assistants API를 통한 분석 사유 및 대응 지침 생성"""
        print(f"[OpenAI] {url} RAG 분석 요청 중...")

        status_text = "악성(큐싱 의심)" if is_malicious_final else "정상"
        prompt = (
            f"(ML 모델 악성 판단 확률: {confidence_score * 100:.1f}%)\n\n"
            f"네가 가진 보안 지침(Vector Store)을 참고해서 판단 사유와 대응 지침을 작성해 줘. "
            f"반드시 마크다운이나 추가 설명 없이 아래 JSON 형식으로만 정확하게 답변해.\n"
            f"{{\n"
            f"  \"reason\": \"위험/안전 판단 상세 사유\",\n"
            f"  \"countermeasures\": [\"대응 지침 1\", \"대응 지침 2\"]\n"
            f"}}"
        )

        try:
            # Thread 생성 및 Message 추가
            thread = self.client.beta.threads.create()
            self.client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=prompt
            )

            # Run 실행 및 대기
            run = self.client.beta.threads.runs.create_and_poll(
                thread_id=thread.id,
                assistant_id=self.assistant_id,
            )

            # 결과 처리
            if run.status == 'completed':
                messages = self.client.beta.threads.messages.list(thread_id=thread.id)
                assistant_response = messages.data[0].content[0].text.value

                # 마크다운 블록(```json) 제거 후 파싱
                clean_json_str = assistant_response.replace("```json", "").replace("```", "").strip()
                parsed_data = json.loads(clean_json_str)

                # schema.py의 AnalysisResult 규격에 맞춰서 반환
                return AnalysisResult(
                    reason=parsed_data.get("reason", "이유를 분석하지 못했습니다."),
                    countermeasures=parsed_data.get("countermeasures", ["대응 지침이 없습니다."])
                )

            elif run.status == 'requires_action':
                # 현재 Assistant가 tool(function calling)을 쓰도록 설정돼 있다면
                # 여기서 별도 처리 로직이 필요함. 지금은 미사용 가정하고 실패 처리.
                print(f"[오류] Run이 tool 실행을 요구함 (requires_action) — 처리 로직 미구현")
                return AnalysisResult(reason="AI가 추가 작업을 요청했지만 처리할 수 없습니다.", countermeasures=[])

            elif run.status in ('failed', 'cancelled', 'expired'):
                print(f"[오류] Run 실패/중단: status={run.status}, last_error={getattr(run, 'last_error', None)}")
                return AnalysisResult(reason=f"AI 분석이 실패했습니다 ({run.status}).", countermeasures=[])

            else:
                # queued, in_progress 등 create_and_poll이 정상적으로 처리했다면
                # 이론상 여기까지 안 오지만, 방어적으로 남겨둠
                print(f"[오류] 예상치 못한 Run 상태: {run.status}")
                return AnalysisResult(reason="AI 분석이 중단되었습니다.", countermeasures=[])

        except json.JSONDecodeError as e:
            # AI가 JSON 형식을 안 지켰을 때 (프롬프트/모델 문제)
            print(f"[오류] AI 응답 JSON 파싱 실패: {e}")
            return AnalysisResult(reason="AI 응답 형식 오류로 분석에 실패했습니다.", countermeasures=["관리자에게 문의하세요."])

        except RateLimitError as e:
            print(f"[오류] OpenAI 요청 한도 초과: {e}")
            return AnalysisResult(reason="일시적으로 요청이 많아 분석에 실패했습니다.", countermeasures=["잠시 후 다시 시도해주세요."])

        except APIConnectionError as e:
            print(f"[오류] OpenAI 서버 연결 실패: {e}")
            return AnalysisResult(reason="AI 서버와 통신할 수 없습니다.", countermeasures=["네트워크 상태를 확인해주세요."])

        except APIError as e:
            print(f"[오류] OpenAI API 오류: {e}")
            return AnalysisResult(reason="AI 서버 오류로 분석에 실패했습니다.", countermeasures=["관리자에게 문의하세요."])

        except Exception as e:
            # 그 외 예상치 못한 오류 (최후의 안전망)
            print(f"[오류] 알 수 없는 오류 발생: {e}")
            return AnalysisResult(reason="서버 통신 오류", countermeasures=["관리자에게 문의하세요."])

    def analyze(self, url: str, detection_result: DetectionResult) -> AnalysisResult:
        """기능 3: 통합 악성 URL 판단 및 최종 결과 반환 (앱팀이 호출할 메인 함수)"""
        
        is_bad_in_db = self.check_external_database(url)
        # ML 모델 결과와 외부 DB 결과를 종합해서 최종 판단
        is_malicious_final = detection_result.is_malicious or is_bad_in_db
        
        if is_malicious_final:
            self.register_malicious_url(url)
            
        return self.generate_rag_response(url, is_malicious_final, detection_result.confidence_score)

# ---------------------------------------------------------
# 단독 테스트 실행 코드
# ---------------------------------------------------------
if __name__ == "__main__":
    engine = RAGEngine()
    
    # schema.py의 DetectionResult 객체를 가상으로 생성해서 테스트
    mock_detection = DetectionResult(is_malicious=True, confidence_score=0.92)
    test_url = "http://g00gle-login.com:8080/verify"
    # 통합 분석 실행
    final_report = engine.analyze(url=test_url, detection_result=mock_detection)
    
    print("\n[ 최종 앱 전달용 데이터 ]")
    print(f"Reason: {final_report.reason}")
    print(f"Countermeasures: {final_report.countermeasures}")