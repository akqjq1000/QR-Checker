import streamlit as st
from modules import feature_extractor_dummy as feature_extractor
from modules import ml_detector_dummy as ml_detector
from modules import rag_engine_dummy as rag_engine


from modules.schema import AnalysisResult, ScanReport, FeatureVector

st.set_page_config(page_title="QR-Shield", page_icon="")
st.title("QR-Shield")

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
def build_report(url: str) -> ScanReport:
    features = feature_extractor.extract(url)
    detection = ml_detector.predict(features)
    with st.spinner("보안 지침 문서를 검색해 분석하는 중..."):
        analysis = rag_engine.analyze(url, features, detection)
    return ScanReport(url=url, features=features, detection=detection, analysis=analysis)


# ===========================================================
# 화면
# ===========================================================
with st.sidebar:
    st.header("입력")
    url_input = st.text_input("검사할 URL")
    run = st.button("분석 시작", type="primary", use_container_width=True)

if run:
    report = build_report(url_input)
    st.session_state["last_report"] = report
 
if "last_report" in st.session_state:
    render_report(st.session_state["last_report"])
else:
    st.info("사이드바에서 URL을 입력하고 '분석 시작'을 눌러주세요.")
