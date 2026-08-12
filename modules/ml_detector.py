import joblib
import numpy as np
from schema import FeatureVector, DetectionResult

class MaliciousURLDetector:
    # model_path: str = '../models/url_classifier.pkl'
    def __init__(self, model_path: str = '../models/url_classifier.pkl'):
        try:
            self.model = joblib.load(model_path)
            print(f"[ML_Detector] 모델 로드 완료: {model_path}")
        except FileNotFoundError:
            print(f"[ML_Detector] 오류: {model_path} 파일을 찾을 수 없습니다.")
            self.model = None

    def predict(self, features: FeatureVector) -> DetectionResult:
        """
        FeatureVector를 입력받아 XGBoost 모델로 예측한 뒤,
        DetectionResult 객체로 반환합니다.
        """
        if self.model is None:
            raise ValueError("모델이 로드되지 않았습니다.")

        # 1. FeatureVector를 ML 모델 입력용 2차원 Numpy 배열로 변환
        # to_array()는 1D 리스트를 반환하므로, 
        # 단일 데이터 예측을 위해 shape을 (1, 16)으로 맞춰줍니다.
        feature_array = np.array([features.to_array()])

        # 2. 모델 예측 (확률 계산)
        # predict_proba는 [[정상일 확률, 악성일 확률]] 형태의 2차원 배열을 반환합니다.
        probabilities = self.model.predict_proba(feature_array)[0]
        
        # 악성(클래스 1)일 확률을 추출합니다.
        confidence_score = float(probabilities[1])

        # 3. 임계값(Threshold)을 통한 이진 판단
        # 악성 확률이 0.5 이상 ($ P(\text{malicious}) \ge 0.5 $)이면 악성으로 판단합니다.
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
    # 임시 피처 생성 (schema.py의 예시 활용)
    sample_features = FeatureVector(
        len_url=35, len_sub_domain=6, len_root_domain=15, len_suffix=3,
        len_encoding=0, len_query=6,
        count_sub_domain=1, count_file_path=1, count_special_char=5, count_url_dots=3,
        is_ip=False, is_private=False, is_filter=True, num_port=8080,
        ratio_alpha_numeric=0.82, value_entropy_url=3.94,
    )

    # 탐지기 객체 생성 및 예측
    detector = MaliciousURLDetector('xgboost_malicious_url_model.pkl')
    
    # 예측 수행 (FeatureVector 입력 -> DetectionResult 출력)
    result = detector.predict(sample_features)
    
    print("\n[ 예측 결과 ]")
    print(f"악성 여부: {result.is_malicious}")
    print(f"악성 확률: {result.confidence_score * 100:.2f}%")