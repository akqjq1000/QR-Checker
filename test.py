import streamlit as st
from pathlib import Path

import modules.qr_decoder as qr_decoder
from modules.ml_detector import MaliciousURLDetector
from modules.AI_RAG.rag_engine4 import RAGEngine
from modules.url_to_feature import extract_features
from modules.web_screenshot import capture_website

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
            ml_detector = MaliciousURLDetector()
            detection_result = ml_detector.predict(features=features)

            # 스캔 결과를 세션에 저장
            st.session_state.scan_result = {
                "url": url,
                "detection": detection_result,
                "features": features
            }

            # 악성일 경우 RAG 엔진 초기화 (채팅 시작)
            if detection_result.is_malicious:
                rag_response = st.session_state.rag_engine.init_scan(url, detection_result)
                st.session_state.chat_session_id = rag_response['session_id']
                # 첫 번째 메시지(분석 결과 알림)를 채팅 기록에 추가
                st.session_state.chat_history = [{"role": "assistant", "content": rag_response['message']}]
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
    url = res['url']
    detection = res['detection']
    features = res['features']

    st.markdown("---")
    st.subheader("🔍 분석 대상")
    # 클릭 가능한 URL 버튼: 클릭 시 스크린샷 생성 및 미리보기
    if 'screenshot_path' not in st.session_state:
        st.session_state.screenshot_path = None

    if st.button(url, key=f"preview_{url}"):
        with st.spinner("웹페이지 미리보기 생성 중..."):
            try:
                result_path = capture_website(url)
                if result_path:
                    st.session_state.screenshot_path = result_path
                else:
                    st.session_state.screenshot_path = None
                    st.error("웹페이지 미리보기를 생성하지 못했습니다.")
            except Exception as e:
                st.session_state.screenshot_path = None
                st.error(f"미리보기 생성 중 오류: {e}")

    # 스크린샷이 생성되어 있으면 표시
    if st.session_state.get('screenshot_path'):
        with st.expander("웹페이지 미리보기 (스크린샷)"):
            st.image(st.session_state.screenshot_path, width='content')

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
                    
                    if rag_response['status'] == 'completed':
                        # 최종 결과 생성 및 기록 추가
                        analysis = rag_response['result']
                        final_msg = (f"**[최종 분석 결과]**\n\n{analysis.reason}\n\n"
                                     f"**대응 지침:**\n• " + "\n• ".join(analysis.countermeasures))
                        st.session_state.chat_history.append({"role": "assistant", "content": final_msg})
                        st.session_state.chat_session_id = None # 세션 종료
                    else:
                        # 기타 상태 처리
                        st.session_state.chat_history.append({"role": "assistant", "content": rag_response['message']})
                
                st.rerun() # 화면 갱신을 위해 리런

    else:
        # 정상 URL일 경우 성공 메시지 및 피처 표시
        st.success(f"✅ 안전한 URL입니다. (악성 확률: {detection.confidence_score*100:.2f}%)")
        with st.expander("추출된 URL 피처 보기"):
            st.json(features.to_dict())