import streamlit as st
from pathlib import Path

import modules.qr_decoder as qr_decoder
from modules.ml_detector import MaliciousURLDetector
from modules.AI_RAG.rag_engine4 import RAGEngine
from modules.url_to_feature import extract_features
from modules.web_screenshot import capture_website
from modules.schema import ScanReport, AnalysisResult, FeatureVector, DetectionResult

st.title("QR-Checker")
st.caption('큐싱을 예방하기 위한 QR 코드 분석 및 대응 방안 안내 프로그램 입니다.')

# 1. 세션 상태 초기화 (상태 유지를 위해 필수)
if 'rag_engine' not in st.session_state:
    st.session_state.rag_engine = RAGEngine()
if 'scan_result' not in st.session_state:
    st.session_state.scan_result = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'chat_session_id' not in st.session_state:
    st.session_state.chat_session_id = None

# 이미지 
img = st.file_uploader("QR 코드 이미지를 업로드하세요", type=["png", "jpg", "jpeg"])
analysis_btn = st.button('분석', type='primary')

# 2. 분석 로직 (버튼 클릭 시 실행)
if analysis_btn and img:
    try:
        DATA_DIR = Path(__file__).parent / "data/qr-image"
        DATA_DIR.mkdir(exist_ok=True) # 데이터 폴더가 없으면 생성
        save_path = DATA_DIR / img.name
        save_path.write_bytes(img.getvalue())

        # QR 디코딩 (경로를 문자열로 전달)
        url = qr_decoder.extract_url_from_qr(str(save_path))

        if url:
            features = extract_features(url)
            # Ensure features is FeatureVector
            if not isinstance(features, FeatureVector):
                try:
                    features = FeatureVector(**features)
                except Exception:
                    pass
            ml_detector = MaliciousURLDetector()
            detection_result = ml_detector.predict(features=features)
            # Ensure detection_result is DetectionResult
            if not isinstance(detection_result, DetectionResult):
                try:
                    detection_result = DetectionResult(**detection_result)
                except Exception:
                    pass

            # 호출: 항상 RAG 엔진에 초기 스캔 요청을 전달하고 모듈이 반환하는 값을 그대로 사용
            rag_response = st.session_state.rag_engine.init_scan(url, detection_result)

            # Normalize possible return formats from modules (dict or tuple)
            # Expected dict form: {"status": "completed"/"chat_required", ...}
            # Expected tuple form: ('completed', AnalysisResult) or ('chat_required', session_id, message)
            status = None
            analysis = None
            session_id = None
            message = None

            if isinstance(rag_response, dict):
                status = rag_response.get('status')
                if status == 'completed':
                    analysis = rag_response.get('result')
                elif status == 'chat_required':
                    session_id = rag_response.get('session_id')
                    message = rag_response.get('message')
            elif isinstance(rag_response, (list, tuple)):
                if len(rag_response) >= 1:
                    status = rag_response[0]
                    if status == 'completed' and len(rag_response) >= 2:
                        analysis = rag_response[1]
                    elif status == 'chat_required' and len(rag_response) >= 3:
                        session_id = rag_response[1]
                        message = rag_response[2]

            # If analysis provided as dict, coerce to AnalysisResult
            if analysis and not isinstance(analysis, AnalysisResult) and isinstance(analysis, dict):
                try:
                    analysis = AnalysisResult(**analysis)
                except Exception:
                    analysis = AnalysisResult(reason=str(analysis), countermeasures=[])

            # Store ScanReport; if chat is required and no analysis yet, store analysis as None
            st.session_state.scan_result = ScanReport(url=url, features=features, detection=detection_result, analysis=analysis)

            if status == 'completed':
                st.session_state.chat_session_id = None
                st.session_state.chat_history = []
            elif status == 'chat_required':
                st.session_state.chat_session_id = session_id
                st.session_state.chat_history = [{"role": "assistant", "content": message or "추가 정보가 필요합니다."}]
            else:
                st.session_state.chat_session_id = None
                st.session_state.chat_history = []

        else:
            st.warning('추출된 URL이 없습니다. 선명한 이미지를 사용해주세요.')
    except Exception as e:
        st.error(f'오류 발생: {e}')

# 3. 결과 및 채팅 인터페이스 출력
if st.session_state.scan_result:
    res = st.session_state.scan_result
    url = res.url
    detection = res.detection
    features = res.features

    st.markdown("---")
    st.subheader("🔍 분석 대상")
    # 클릭 가능한 URL 버튼: 클릭 시 스크린샷 생성 및 미리보기
    if 'screenshot_path' not in st.session_state:
        st.session_state.screenshot_path = None

    # 악성 URL의 경우 문제가 있을 수 있어서 임시 수정
    # if st.button(url, key=f"preview_{url}"):
    #     with st.spinner("웹페이지 미리보기 생성 중..."):
    #         try:
    #             result_path = capture_website(url)
    #             if result_path:
    #                 st.session_state.screenshot_path = result_path
    #             else:
    #                 st.session_state.screenshot_path = None
    #                 st.error("웹페이지 미리보기를 생성하지 못했습니다.")
    #         except Exception as e:
    #             st.session_state.screenshot_path = None
    #             st.error(f"미리보기 생성 중 오류: {e}")

    # # 스크린샷이 생성되어 있으면 표시
    # if st.session_state.get('screenshot_path'):
    #     with st.expander("웹페이지 미리보기 (스크린샷)"):
    #         st.image(st.session_state.screenshot_path, width='content')

    if detection.is_malicious:
        # 악성 판정 시 경고 메시지 출력
        st.error(f"⚠️ 악성 URL 의심 (확률: {detection.confidence_score*100:.2f}%)")
        
        # 채팅 기록 표시
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        # 채팅 입력창 (세션 ID가 있을 때만 활성화)
        if st.session_state.chat_session_id:
            user_input = st.chat_input("질문을 입력하세요 (예: 접속했어요, 아니요)")
            if user_input:
                # 사용자 메시지 추가 및 표시
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                with st.chat_message("user"):
                    st.write(user_input)

                # RAG 엔진을 통한 대화 처리
                with st.spinner("AI 분석 중..."):
                    rag_response = st.session_state.rag_engine.chat(st.session_state.chat_session_id, user_input)

                    # Normalize possible return formats (dict or tuple)
                    c_status = None
                    c_analysis = None
                    c_message = None
                    c_session = None

                    if isinstance(rag_response, dict):
                        c_status = rag_response.get('status')
                        if c_status == 'completed':
                            c_analysis = rag_response.get('result')
                        else:
                            c_message = rag_response.get('message')
                    elif isinstance(rag_response, (list, tuple)):
                        if len(rag_response) >= 1:
                            c_status = rag_response[0]
                            if c_status == 'completed' and len(rag_response) >= 2:
                                c_analysis = rag_response[1]
                            elif c_status == 'chat_required' and len(rag_response) >= 3:
                                c_session = rag_response[1]
                                c_message = rag_response[2]
                    
                    if c_status == 'completed' and c_analysis is not None:
                        # coerce analysis if dict
                        if not isinstance(c_analysis, AnalysisResult) and isinstance(c_analysis, dict):
                            try:
                                c_analysis = AnalysisResult(**c_analysis)
                            except Exception:
                                c_analysis = AnalysisResult(reason=str(c_analysis), countermeasures=[])

                        # update stored ScanReport.analysis
                        if isinstance(st.session_state.get('scan_result'), ScanReport):
                            st.session_state.scan_result.analysis = c_analysis

                        final_msg = (f"**[최종 분석 결과]**\n\n{c_analysis.reason}\n\n"
                                     f"**대응 지침:**\n• " + "\n• ".join(c_analysis.countermeasures))
                        st.session_state.chat_history.append({"role": "assistant", "content": final_msg})
                        st.session_state.chat_session_id = None

                    elif c_status == 'chat_required':
                        # continue chat — append message if provided
                        msg = c_message or rag_response if isinstance(rag_response, str) else c_message
                        st.session_state.chat_history.append({"role": "assistant", "content": msg})
                        # keep session id
                        if c_session:
                            st.session_state.chat_session_id = c_session

                    else:
                        # error or unexpected
                        msg = None
                        if isinstance(rag_response, dict):
                            msg = rag_response.get('message')
                        st.session_state.chat_history.append({"role": "assistant", "content": msg or "응답 처리 중 오류가 발생했습니다."})
                
                st.rerun() # 화면 갱신을 위해 리런

    else:
        # 정상 URL일 경우 성공 메시지 및 피처 표시
        st.success(f"✅ 안전한 URL입니다. (악성 확률: {detection.confidence_score*100:.2f}%)")
        with st.expander("추출된 URL 피처 보기"):
            st.json(features.to_dict())