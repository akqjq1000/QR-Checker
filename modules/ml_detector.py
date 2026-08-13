import os
import joblib
import numpy as np
import pandas as pd
from schema import *
import xgboost

import random   # 데이터셋에서 랜덤하게 데이터를 뽑아오기 위함

class MaliciousURLDetector:
    # 테스트해보고자 하는 모델을 딕셔너리로 저장
    AVAILABLE_MODELS = {
        'xgboost': 'XGBoost_classifier.pkl',
        'rf': 'RandomForest_classifier.pkl',
        'randomforest': 'RandomForest_classifier.pkl',
        'random forest': 'RandomForest_classifier.pkl',
        'lgbm': 'LightGBM_classifier.pkl',
        'lightgbm': 'LightGBM_classifier.pkl'
    }

    def __init__(self, model_type: str = 'xgboost'):
        # 기본값은 성능이 가장 좋은 'xgboost'로 지정
        model_type = model_type.lower()

        if model_type not in self.AVAILABLE_MODELS:
            raise ValueError(f"오류: '{model_type}'은 아직 없는 모델입니다. {list(self.AVAILABLE_MODELS.keys())}")

        model_filename = self.AVAILABLE_MODELS[model_type]
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(current_dir, '..', 'models', model_filename)

        try:
            self.model = joblib.load(model_path)
            print(f"[ML_Detector] 모델 로드 완료: {model_path}")
        except FileNotFoundError:
            print(f"[ML_Detector] 오류: {model_path} 파일을 찾을 수 없습니다.")
            self.model = None

    def predict(self, features: FeatureVector) -> DetectionResult:
        # FeatureVector를 입력받아 XGBoost 모델로 예측한 뒤, DetectionResult 객체로 반환
        if self.model is None:
            raise ValueError("모델이 로드되지 않았습니다.")

        # 1. FeatureVector를 ML 모델 입력용 2차원 Numpy 배열로 변환
        feature_array = np.array([features.to_array()])

        # 2-1. 모델 예측 (확률 계산)
        probabilities = self.model.predict_proba(feature_array)[0]

        # 2-2. 악성(클래스 1)일 확률을 추출
        confidence_score = float(probabilities[1])

        # 3. 임계값(Threshold)을 통한 이진 판단
        is_malicious = bool(confidence_score >= 0.5)

        # 4. 약속된 스키마인 DetectionResult로 패키징하여 반환
        return DetectionResult(
            is_malicious=is_malicious,
            confidence_score=confidence_score
        )

# ==========================================
# 테스트 코드 (단독 실행 시에만 동작)
# ==========================================
if __name__ == "__main__":
    # 1. 데이터셋 절대 경로 설정
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, '..', 'data', 'train_urls.csv')

    try:
        # 2. 전처리된 데이터 로드
        df = pd.read_csv(data_path) # read_csv가 columns(0번째 행)는 떼고 df를 반환

        # 3. 랜덤으로 하나의 행 추출
        random_index = random.randint(0, len(df) - 1)   # random_index 하드코딩하면 해당 열만 테스트 가능 (다른 모델과 비교 시)
        sample_row = df.iloc[random_index]

        # 4. 추출한 데이터를 FeatureVector 스키마에 맞게 매핑
        sample_features = FeatureVector(
            len_url=int(sample_row['len_url']),
            len_sub_domain=int(sample_row['len_sub_domain']),
            len_root_domain=int(sample_row['len_root_domain']),
            len_suffix=int(sample_row['len_suffix']),
            len_encoding=int(sample_row['len_encoding']),
            len_query=int(sample_row['len_query']),
            count_sub_domain=int(sample_row['count_sub_domain']),
            count_file_path=int(sample_row['count_file_path']),
            count_special_char=int(sample_row['count_special_char']),
            count_url_dots=int(sample_row['count_url_dots']),
            is_ip=bool(sample_row['is_ip']),
            is_private=bool(sample_row['is_private']),
            is_filter=bool(sample_row['is_filter']),
            num_port=int(sample_row['num_port']),
            ratio_alpha_numeric=float(sample_row['ratio_alpha_numeric']),
            value_entropy_url=float(sample_row['value_entropy_url'])
        )

        # 실제 정답 추출
        actual_label = int(sample_row['label'])
        actual_status = "악성(1)" if actual_label == 1 else "정상(0)"

        # 5. 탐지기 객체 생성 및 예측
            # model_type 종류:
            # 'rf' / 'random foreast' / 'randomforest'
            # 'xgboost'
            # 'lgbm' / 'lightgbm'
        detector = MaliciousURLDetector('lgbm')
        # DetectionResult로 패키징된 데이터를 result로 받음 (is_malicious와 confidence_score 있음)
        result = detector.predict(sample_features)

        predicted_status = "악성(True)" if result.is_malicious else "정상(False)"

        # 6. 결과 출력 및 비교
        print(f"\n[ 테스트 데이터 인덱스: {random_index} ]")
        print("-" * 30)
        print(f"실제 정답: {actual_status}")
        print(f"모델 예측: {predicted_status}")
        print(f"악성 확률: {result.confidence_score * 100:.2f}%")
        print("-" * 30)

        if (actual_label == 1 and result.is_malicious) or (actual_label == 0 and not result.is_malicious):
            print("예측 성공")
        else:
            print("예측 실패")

    except FileNotFoundError:
        print(f"데이터 파일을 찾을 수 없습니다: {data_path}")