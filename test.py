import streamlit as st
from pathlib import Path
import requests

import modules.qr_decoder as qr_decoder
from modules.ml_detector import MaliciousURLDetector
from modules.AI_RAG.rag_engine5 import RAGEngine
from modules.url_to_feature import extract_features
from modules.url_resolver import resolve_url, URLResolutionError
from modules.schema import ScanReport, AnalysisResult, FeatureVector, DetectionResult

# 웹 타이틀과 설명
st.title("QR-Checker")
st.caption('큐싱을 예방하기 위한 QR 코드 분석 및 대응 방안 안내 프로그램 입니다.')

# 1. 세션 상태 초기화 (상태 유지를 위해 필수)
if 'rag_engine' not in st.session_state: # RAG 엔진
    with st.spinner('RAG 엔진 로드 중...'):
        st.session_state.rag_engine = RAGEngine()
if 'ml_detector' not in st.session_state: # ML 검사기
    # 모델 종류
    # AVAILABLE_MODELS = {
    #         'xgboost': 'XGBoost_classifier.pkl',
    #         'rf': 'RandomForest_classifier.pkl',
    #         'randomforest': 'RandomForest_classifier.pkl',
    #         'random forest': 'RandomForest_classifier.pkl',
    #         'lgbm': 'LightGBM_classifier.pkl',
    #         'lightgbm': 'LightGBM_classifier.pkl'
    #     }
    with st.spinner('모델 로드 중...'):
        st.session_state.ml_detector = MaliciousURLDetector('rf')
if 'scan_result' not in st.session_state: # 검사 결과
    st.session_state.scan_result = None
if 'chat_history' not in st.session_state: # 채팅 기록
    st.session_state.chat_history = []
if 'chat_session_id' not in st.session_state: # OpenAI 채팅 세션
    st.session_state.chat_session_id = None
if 'last_file_name' not in st.session_state: # 업로드 파일 이름
    st.session_state.last_file_name = None
if 'enable_web_screenshot' not in st.session_state:
    st.session_state.enable_web_screenshot = True

if st.toggle('웹 미리보기 기능 활성화', value=st.session_state.enable_web_screenshot):
    st.session_state.enable_web_screenshot = True
else:
    st.session_state.enable_web_screenshot = False

# 이미지 업로드
img = st.file_uploader("QR 코드 이미지를 업로드하세요", type=["png", "jpg", "jpeg"])

# 이미지를 변경하거나 지울 때
if img is not None:
    if st.session_state.last_file_name != img.name:
        st.session_state.last_file_name = img.name
        st.session_state.scan_result = None
        st.session_state.screenshot_path = None
else:
    st.session_state.last_file_name = None
    st.session_state.scan_result = None
    st.session_state.screenshot_path = None

analysis_btn = st.button('분석하기', type='primary')

# 2. 분석 로직 (버튼 클릭 시 실행)
if analysis_btn and img:
    try:
        # 이미지 저장 경로 분리
        DATA_DIR = Path(__file__).parent / "data/qr-image"
        DATA_DIR.mkdir(exist_ok=True) # 데이터 폴더가 없으면 생성
        save_path = DATA_DIR / img.name
        save_path.write_bytes(img.getvalue()) # 이미지 값만 추출하여 저장

        # QR 디코딩 (경로를 문자열로 전달)
        url = qr_decoder.extract_url_from_qr(str(save_path))

        if url: # URL이 확인되면
            # 짧은 URL 풀기
            try:
                resolved = resolve_url(url)
                if resolved and resolved != url:
                    st.info(f'단축 URL 탐지(원본: {url})')
                    url = resolved
            except URLResolutionError as e:
                # 리디렉트 추적 실패 시 경고를 남기고 원본 URL로 진행
                st.warning(f"URL 확장 오류: {e}. 원본 URL로 검사합니다.")
            features = extract_features(url) # 피처 추출
            if not isinstance(features, FeatureVector): # 결과값 검증
                try:
                    # 피처 변수를 다시 등록하여 정상 적인 피처 변수로 변환
                    features = FeatureVector(**features) 
                except Exception:
                    pass
            # 추출된 피처 넣어서 악성 코드인지 검토
            detection_result = st.session_state.ml_detector.predict(features=features)

            # 결과값 검증
            if not isinstance(detection_result, DetectionResult):
                try:
                    detection_result = DetectionResult(**detection_result)
                except Exception:
                    pass

            # 머신러닝 검사기의 결과와 URL을 넣어서 한 번 더 검증(외부 DB, RAG+chromadb, ML 모델 추가 검증)
            rag_response = st.session_state.rag_engine.init_scan(url, detection_result)

            # st.session_state 변수에 있는 값을 편하게 사용하기 위해서 일반 변수 선언
            status = None
            analysis = None
            session_id = None
            message = None

            if isinstance(rag_response, dict): # 결과값 검증(RAG에서 분석 결과는 dict형태로 보내줌)
                status = rag_response.get('status')
                if status == 'completed': 
                    # 정상적인 URL이 입력되면 더 이상 점검할 내용 없으므로 바로 분석 보고서에 결과 저장
                    analysis = rag_response.get('result') # result는 AnalysisResult 형태로 반환됨
                elif status == 'chat_required':
                    # 만약 악성 URL이라면 사용자와 2번의 채팅을 통해 RAG/파일 서치 + 웹 서치 진행
                    session_id = rag_response.get('session_id') # RAG 파트에서 사용할 세션 아이디
                    message = rag_response.get('message') # RAG 파트에서 제공해준 결과 메시지

            # 응답 결과를 생성할 때 형식이 일치하지 않으면 강제로 맞추는 기능
            if analysis and not isinstance(analysis, AnalysisResult) and isinstance(analysis, dict):
                try:
                    analysis = AnalysisResult(**analysis) # 임시 분석 결과 생성
                except Exception:
                    analysis = AnalysisResult(reason=str(analysis), countermeasures=[]) # 임시 분석 결과 생성

            # 결과 리포트 먼저 만들고 만약 채팅이 필요하다면 추후 처리
            st.session_state.scan_result = ScanReport(url=url, features=features, detection=detection_result, analysis=analysis)

            if status == 'completed':
                st.session_state.chat_session_id = None
                st.session_state.chat_history = []
            elif status == 'chat_required':
                st.session_state.chat_session_id = session_id
                st.session_state.chat_history = [{"role": "assistant", "content": message or "추가 정보가 필요합니다."}]
            else: # 대화 초기화
                st.session_state.chat_session_id = None
                st.session_state.chat_history = []

        else: # URL이 없을 경우
            st.warning('추출된 URL이 없습니다. 선명한 이미지를 사용해주세요.')
    except Exception as e:
        st.error(f'오류 발생: {e}')

# 3. 결과 및 채팅 인터페이스 출력
if st.session_state.scan_result:
    res = st.session_state.scan_result # 검사 결과 불러오기
    url = res.url # 검사 URL
    detection = res.detection # 머신러닝 검사 결과
    features = res.features # 추출된 피처 정보

    st.markdown("---")
    st.subheader("🔍 분석 대상")

    st.write('추출된 URL:', url, unsafe_allow_html=True)

    if 'screenshot_path' not in st.session_state:
        st.session_state.screenshot_path = None

    if st.session_state.enable_web_screenshot:
        st.write('#### 샌드박스 추출로 안전한 미리보기')
        if st.button(url, key=f"preview_{url}", disabled=(st.session_state.screenshot_path != None)):
            with st.spinner("웹페이지 미리보기 생성 중..."):
                try:
                    response = requests.post('http://localhost:8000/capture/', headers={'Content-Type': 'application/json'}, json={'url': url})
                
                    # 3. 요청 성공 시 이미지 파일로 저장 (헤더에서 파일명 추출)
                    if response.status_code == 200:
                        # Content-Disposition 헤더에서 filename="파일명" 부분 추출
                        cd = response.headers.get('Content-Disposition', '')
                        file_name = cd.split('filename=')[1].strip('"') if 'filename=' in cd else "captured_image.png"
                        # 이미지 저장 경로 지정
                        SITE_IMAGE_DIR = Path(__file__).parent / 'data/site-image'
                        site_image_path = SITE_IMAGE_DIR / file_name

                        with open(site_image_path, "wb") as f:
                            f.write(response.content)
                        
                        st.session_state.screenshot_path = site_image_path # 이미지 저장 경로 저장
                    else:
                        st.error(f"요청 실패 (상태 코드: {response.status_code})")
                        st.session_state.screenshot_path = None

                except Exception as e:
                    st.session_state.screenshot_path = None
                    st.error(f"미리보기 생성 중 오류: {e}")

        # 스크린샷이 생성되어 있으면 표시
        if st.session_state.get('screenshot_path'):
            with st.expander("웹페이지 미리보기 (스크린샷)", expanded=True):
                st.image(st.session_state.screenshot_path, width='content')

    # 악성 의심 URL일 경우
    if detection.is_malicious:
        # 악성 판정 시 경고 메시지 출력
        st.error(f"⚠️ 악성 URL 의심 (확률: {detection.confidence_score*100:.2f}%)")
        
        # 채팅 기록 표시
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        # 채팅 입력창 (세션 ID가 있을 때만 활성화)
        if st.session_state.chat_session_id:
            # 사용자 입력 받기
            user_input = st.chat_input("질문을 입력하세요 (예: 접속했어요, 아니요)")
            if user_input:
                # 사용자 메시지 가공하여 전달
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                with st.chat_message("user"):
                    st.write(user_input)

                # RAG 엔진을 통한 대화 처리
                with st.spinner("AI 분석 중..."):
                    rag_response = st.session_state.rag_engine.chat(st.session_state.chat_session_id, user_input)

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
                    
                    # RAG 엔진 내부 처리 결과 완료 상태이고 결과값이 제공 되었다면
                    if c_status == 'completed' and c_analysis is not None:
                        # 응답 결과를 생성할 때 형식이 일치하지 않으면 강제로 맞추는 기능
                        if not isinstance(c_analysis, AnalysisResult) and isinstance(c_analysis, dict):
                            try:
                                c_analysis = AnalysisResult(**c_analysis)
                            except Exception:
                                c_analysis = AnalysisResult(reason=str(c_analysis), countermeasures=[])

                        # ScanReport로 받아 세션의 scan_result와 동일한 형식인지 검사
                        if isinstance(st.session_state.get('scan_result'), ScanReport):
                            st.session_state.scan_result.analysis = c_analysis # 최종 분석 결과를 저장

                        # 최종 분석 결과
                        final_msg = (f"**[최종 분석 결과]**\n\n{c_analysis.reason}\n\n"
                                     f"**대응 지침:**\n\n• " + "\n\n• ".join(c_analysis.countermeasures))
                        st.session_state.chat_history.append({"role": "assistant", "content": final_msg})
                        st.session_state.chat_session_id = None

                    elif c_status == 'chat_required':
                        # 처음 질문에 예를 답한 경우
                        msg = c_message or rag_response if isinstance(rag_response, str) else c_message
                        st.session_state.chat_history.append({"role": "assistant", "content": msg})

                        # 세션 ID 유지하여 기존 응답 기억
                        if c_session:
                            st.session_state.chat_session_id = c_session

                    else:
                        # 만약 상태 정보가 일치하는 게 없다면 오류
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