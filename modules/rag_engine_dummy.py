import uuid

from modules.schema import AnalysisResult, DetectionResult

# 실제 rag_engine.py와 동일하게 세션 상태를 모듈 레벨 딕셔너리로 관리 (더미이므로 인메모리로 충분)
sessions = {}


class RAGEngine:
    """rag_engine.py의 인터페이스(init_scan/chat)를 흉내 내는 MOCK 엔진.
    실제 OpenAI 호출 없이 고정된 응답으로 대화 흐름만 재현."""

    def init_scan(self, url: str, detection_result: DetectionResult) -> dict:
        if not detection_result.is_malicious:
            return {
                "status": "completed",
                "result": AnalysisResult(
                    reason=f"입력된 URL('{url}')은 주요 피싱 특성이 발견되지 않은 정상적인 형태입니다.",
                    countermeasures=["특이사항 없음"],
                ),
            }

        session_id = str(uuid.uuid4())
        sessions[session_id] = {"url": url, "state": "ASKED_ACCESS"}

        return {
            "status": "chat_required",
            "session_id": session_id,
            "message": (
                f"위험한 QR로 판정되었습니다! ({detection_result.confidence_score * 100:.1f}%)\n"
                "해당 링크에 접속하셨나요? (예/아니오)"
            ),
        }

    def chat(self, session_id: str, user_message: str) -> dict:
        if session_id not in sessions:
            return {"status": "error", "message": "유효하지 않거나 만료된 세션입니다."}

        session_data = sessions[session_id]
        state = session_data["state"]

        if state == "ASKED_ACCESS":
            if "아니" in user_message or "안" in user_message:
                del sessions[session_id]
                return {
                    "status": "completed",
                    "result": AnalysisResult(
                        reason="사용자가 악성 링크에 접속하지 않았습니다.",
                        countermeasures=[
                            "해당 QR 이미지를 즉시 삭제하세요.",
                            "출처가 확인되지 않은 QR은 스캔하지 마세요.",
                        ],
                    ),
                }

            session_data["state"] = "ASKED_ACTION"
            return {
                "status": "chat_required",
                "session_id": session_id,
                "message": (
                    "어떤 페이지였거나, 어떤 행동을 하셨나요?\n"
                    "1. 로그인/비밀번호 입력\n2. 파일(.apk, .exe 등) 다운로드\n3. 단순 접속만 한 뒤 닫음"
                ),
            }

        if state == "ASKED_ACTION":
            del sessions[session_id]
            return {
                "status": "completed",
                "result": AnalysisResult(
                    reason=f"사용자가 링크에 접속했으며 다음 행동을 했습니다: {user_message}",
                    countermeasures=[
                        "관련 계정의 비밀번호를 즉시 변경하세요.",
                        "기기에서 백신 검사를 실행하세요.",
                        "금융 계정에 이상 거래가 없는지 확인하세요.",
                    ],
                ),
            }

        return {"status": "error", "message": "알 수 없는 상태입니다."}
