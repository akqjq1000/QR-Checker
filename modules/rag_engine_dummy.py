from modules.schema import FeatureVector, DetectionResult, AnalysisResult

def analyze(url: str, features: FeatureVector, detection: DetectionResult) -> AnalysisResult:
    """RAG 기반 심층 분석 결과를 생성하는 MOCK 함수"""
    if detection.is_malicious:
        return AnalysisResult(
            reason=f"입력된 URL('{url}')에서 정상 도메인을 위장한 패턴 및 피싱 유도 키워드가 포함되어 있습니다.",
            countermeasures=[
                "해당 링크를 클릭하지 마세요.",
                "이미 접속했다면 즉시 계정 비밀번호를 변경하세요.",
                "공식 앱이나 북마크로만 로그인하세요."
            ]
        )
    else:
        return AnalysisResult(
            reason=f"입력된 URL('{url}')은 주요 피싱 특성이 발견되지 않은 정상적인 형태입니다.",
            countermeasures=[
                "의심스러운 상황이 아니라면 정상적으로 이용 가능합니다."
            ]
        )