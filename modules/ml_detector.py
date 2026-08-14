import os
import random  # 데이터셋에서 랜덤하게 데이터를 뽑아오기 위함

import joblib
import numpy as np
import pandas as pd

from .domain_similarity import extract_root_domain, load_whitelist
from .schema import DetectionResult, FeatureVector
from .url_to_feature import extract_features


class MaliciousURLDetector:
    # 테스트해보고자 하는 모델을 딕셔너리로 저장
    AVAILABLE_MODELS = {  # noqa: RUF012
        "xgboost": "XGBoost_classifier.pkl",
        "rf": "RandomForest_classifier.pkl",
        "randomforest": "RandomForest_classifier.pkl",
        "random forest": "RandomForest_classifier.pkl",
        "lgbm": "LightGBM_classifier.pkl",
        "lightgbm": "LightGBM_classifier.pkl",
    }

    def __init__(self, model_type: str = "xgboost"):
        # 기본값은 성능이 가장 좋은 'xgboost'로 지정
        model_type = model_type.lower()
        if model_type not in self.AVAILABLE_MODELS:
            raise ValueError(
                f"오류: '{model_type}'은 아직 없는 모델입니다. {list(self.AVAILABLE_MODELS.keys())}"
            )
        model_filename = self.AVAILABLE_MODELS[model_type]
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(current_dir, "..", "models", model_filename)
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
            is_malicious=is_malicious, confidence_score=confidence_score
        )

    def predict_url(self, url: str) -> DetectionResult:
        """URL 문자열을 직접 입력받아 피처 추출 후 예측까지 한 번에 수행.

        화이트리스트 도메인과 완전히 일치하면 ML 추론 없이 즉시 안전 판정.
        """
        root = extract_root_domain(url)
        if root in load_whitelist():
            return DetectionResult(is_malicious=False, confidence_score=0.0)

        features = extract_features(url)
        return self.predict(features)


def test_random_sample(detector: MaliciousURLDetector, df: pd.DataFrame) -> None:
    """데이터셋에서 랜덤 샘플 하나 뽑아 테스트"""
    random_index = random.randint(
        0, len(df) - 1
    )  # random_index 하드코딩하면 해당 열만 테스트 가능 (다른 모델과 비교 시)
    sample_row = df.iloc[random_index]
    sample_features = FeatureVector(
        len_url=int(sample_row["len_url"]),
        len_sub_domain=int(sample_row["len_sub_domain"]),
        len_root_domain=int(sample_row["len_root_domain"]),
        len_suffix=int(sample_row["len_suffix"]),
        len_encoding=int(sample_row["len_encoding"]),
        len_query=int(sample_row["len_query"]),
        count_sub_domain=int(sample_row["count_sub_domain"]),
        count_file_path=int(sample_row["count_file_path"]),
        count_special_char=int(sample_row["count_special_char"]),
        count_url_dots=int(sample_row["count_url_dots"]),
        is_ip=bool(sample_row["is_ip"]),
        is_private=bool(sample_row["is_private"]),
        is_filter=bool(sample_row["is_filter"]),
        num_port=int(sample_row["num_port"]),
        ratio_alpha_numeric=float(sample_row["ratio_alpha_numeric"]),
        value_entropy_url=float(sample_row["value_entropy_url"]),
        domain_similarity=float(sample_row["domain_similarity"]),
    )
    actual_label = 1 if sample_row["label"] == "bad" else 0
    actual_status = "악성(1)" if actual_label == 1 else "정상(0)"

    result = detector.predict(sample_features)
    predicted_status = "악성(1)" if result.is_malicious else "정상(0)"

    print("\n[데이터셋 샘플 테스트]")
    print(
        f"실제: {actual_status} / 예측: {predicted_status} (확률 {result.confidence_score:.4f})"
    )


def test_manual_url(detector: MaliciousURLDetector) -> None:
    """사용자가 직접 URL을 입력해서 테스트"""
    url = input("\n테스트할 URL을 입력하세요: ").strip()
    if not url:
        print("URL이 입력되지 않았습니다.")
        return
    try:
        result = detector.predict_url(url)
        status = "악성(1)" if result.is_malicious else "정상(0)"
        print(f"URL: {url}")
        print(f"판정: {status} (악성 확률 {result.confidence_score:.4f})")
    except Exception as e:  # noqa: BLE001
        print(f"[오류] URL 처리 중 문제 발생: {e}")


# ==========================================
# 테스트 코드 (단독 실행 시에만 동작)
# ==========================================
if __name__ == "__main__":
    # 1. 데이터셋 절대 경로 설정
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, "..", "data", "train_urls.csv")

    # model_type 종류:
    # 'rf' / 'random foreast' / 'randomforest'
    # 'xgboost'
    # 'lgbm' / 'lightgbm'
    detector = MaliciousURLDetector("XGBoost")

    while True:
        print("\n" + "=" * 40)
        print("1. 데이터셋 랜덤 샘플 테스트")
        print("2. URL 직접 입력해서 테스트")
        print("3. 종료")
        choice = input("선택: ").strip()

        if choice == "1":
            try:
                df = pd.read_csv(data_path)
                test_random_sample(detector, df)
            except FileNotFoundError:
                print(f"[오류] {data_path} 파일을 찾을 수 없습니다.")
        elif choice == "2":
            test_manual_url(detector)
        elif choice == "3":
            break
        else:
            print("잘못된 입력입니다.")
