from pathlib import Path

import streamlit as st
import modules.qr_decoder as qr_decoder
from modules.ml_detector import MaliciousURLDetector
from modules.url_to_feature import extract_features
from modules.AI_RAG.rag_engine5 import RAGEngine

from modules.schema import AnalysisResult, ScanReport, FeatureVector

st.set_page_config(page_title="QR-Shield", page_icon="")
st.title("QR-Shield")

DATA_DIR = Path(__file__).parent / "data"
rag_engine = RAGEngine()

# ===========================================================
# 렌더링 함수 
# ===========================================================

def render_verdict(report: ScanReport) -> None:
    # 스캔한 URL과 악성/정상 판정. 
    st.markdown(f"**스캔 대상:** '{report.url}")

    score = report.detection.confidence_score
    if report.detection.is_malicious:
        st.error(f"악성 URL로 판정 (악성 확률 {score:.1%})")
    else:
        st.success(f"안전한 URL로 판정 (악성 확률 {score:.1%})")

def render_analysis(analysis: AnalysisResult) -> None:
    # AnalysisResult 출력
    st.subheader("판단 사유")
    st.write(analysis.reason)

    if analysis.countermeasures:
        st.subheader("대응 방안")
        for i, step in enumerate(analysis.countermeasures, 1):
            st.markdown(f"**{i}.** {step}")

def render_feature(features: FeatureVector) -> None:
    # 하단(접이식): 개발자용 피처 상세.
    with st.expander("추출된 URL 피처 보기"):
        st.json(features.to_dict())

def render_report(report: ScanReport) -> None:
    # ScanReport 렌더링
    render_verdict(report)
    st.divider()
    render_analysis(report.analysis)
    st.divider()
    render_feature(report.features)

# ===========================================================
# 파이프라인
# ===========================================================
def analyze_url(url: str) -> None:
    """URL을 받아 피처 추출·탐지까지 수행하고, RAG 상담 세션을 시작."""
    features = extract_features(url)
    ml_detector = MaliciousURLDetector()
    detection = ml_detector.predict(features=features)
    st.session_state["pending"] = {"url": url, "features": features, "detection": detection}

    with st.spinner("보안 지침 문서를 검색해 분석하는 중..."):
        result = rag_engine.init_scan(url, detection)
    _handle_rag_result(result)

def _handle_rag_result(result: dict) -> None:
    """RAG 엔진 응답을 해석해 최종 리포트를 완성하거나, 사용자 답변 대기 상태로 전환."""
    if result["status"] == "completed":
        pending = st.session_state.pop("pending")
        st.session_state["last_report"] = ScanReport(
            url=pending["url"],
            features=pending["features"],
            detection=pending["detection"],
            analysis=result["result"],
        )
        st.session_state.pop("chat_session_id", None)
        st.session_state.pop("chat_message", None)
    else:  # chat_required — 대응방침을 받기 전 사용자 응답이 필요
        st.session_state["chat_session_id"] = result["session_id"]
        st.session_state["chat_message"] = result["message"]

# ===========================================================
# 화면
# ===========================================================
st.header("입력")
qr_image = st.file_uploader("QR 코드 이미지를 업로드하세요", type=["png", "jpg", "jpeg"])
save = st.button("저장", type="primary")

if save and qr_image is not None:
    save_path = DATA_DIR / qr_image.name
    save_path.write_bytes(qr_image.getvalue())
    st.success(f"저장 완료: {save_path}")

    url = qr_decoder.extract_url_from_qr(save_path)
    if url is None:
        st.warning("QR 코드에서 URL을 인식하지 못했습니다.")
    else:
        analyze_url(url)

if "chat_session_id" in st.session_state:
    st.divider()
    st.subheader("추가 확인이 필요합니다")
    st.markdown(st.session_state["chat_message"])
    user_reply = st.chat_input("답변을 입력하세요")
    if user_reply:
        result = rag_engine.chat(st.session_state["chat_session_id"], user_reply)
        _handle_rag_result(result)
        st.rerun()

if "last_report" in st.session_state:
    render_report(st.session_state["last_report"])
else:
    st.info("QR 코드 이미지를 업로드하고 '저장'을 눌러주세요.")