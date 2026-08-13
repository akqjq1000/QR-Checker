from modules.schema import FeatureVector, DetectionResult

def predict(features: FeatureVector) -> DetectionResult:
    """추출된 피처 기반 ML 예측 MOCK 함수"""
    # 임의 로직: URL 길이가 30자 이상이면 악성으로 판단
    is_malicious = features.len_url >= 15
    score = 0.92 if is_malicious else 0.12
    
    return DetectionResult(
        is_malicious=is_malicious,
        confidence_score=score
    )