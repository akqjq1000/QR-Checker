"""
schema.py
---------
파이프라인 전 단계(QR 디코딩 → 피처 추출 → ML 탐지 → RAG 분석 → Streamlit 출력)가
공통으로 주고받는 데이터 형식을 정의합니다.

각 파트는 이 파일에 정의된 클래스만 주고받으면 되므로,
"딕셔너리 키 이름이 다르다", "타입이 안 맞는다" 같은 통합 오류를 방지할 수 있습니다.
"""

from dataclasses import dataclass, field, asdict
from typing import List


# ----------------------------------------------------------------------
# 1. FeatureVector — QR·피처 처리팀 → ML 탐지 모델팀
# ----------------------------------------------------------------------
@dataclass
class FeatureVector:
    """URL 피처 추출 모듈(feature_extractor.py)의 출력 형식."""

    # --- 길이 관련 ---
    len_url: int                # URL 전체 길이
    len_sub_domain: int         # 서브도메인의 길이
    len_root_domain: int        # 전체 도메인(Root Domain)의 길이
    len_suffix: int             # TLD와 SLD의 길이
    len_encoding: int           # URL 내 인코딩 데이터(%XX 등)의 길이
    len_query: int              # URL 내 쿼리 질의문(? 이후)의 길이

    # --- 개수 관련 ---
    count_sub_domain: int       # 서브도메인의 개수
    count_file_path: int        # 파일 경로 깊이 ('/' 개수)
    count_special_char: int     # 특수문자 개수
    count_url_dots: int         # '.' (닷)의 개수

    # --- 구조적 특징 ---
    is_ip: bool                 # 도메인이 문자열이 아닌 IP 주소 형태인지 여부
    is_private: bool            # private TLD 여부
    is_filter: bool             # 낚시성 필터 단어(login, verify, bank 등) 포함 여부
    num_port: int                # 사용된 포트 번호 (없으면 -1)

    # --- 비율/복잡도 ---
    ratio_alpha_numeric: float  # URL 내 알파벳 대비 숫자 비율
    value_entropy_url: float    # URL 문자열의 엔트로피(복잡도)

    def to_dict(self) -> dict:
        """JSON 직렬화 및 API 응답용."""
        return asdict(self)

    def to_array(self) -> List[float]:
        """scikit-learn / XGBoost 모델 입력용 고정 순서 배열.

        모델 학습 시에도 반드시 이 순서(FEATURE_ORDER)를 그대로 사용해야 합니다.
        """
        return [float(getattr(self, name)) for name in FEATURE_ORDER]


# 모델 입력 시 컬럼 순서 고정 (학습 스크립트와 추론 스크립트가 반드시 동일하게 참조)
FEATURE_ORDER = [
    "len_url",
    "len_sub_domain",
    "len_root_domain",
    "len_suffix",
    "len_encoding",
    "len_query",
    "count_sub_domain",
    "count_file_path",
    "count_special_char",
    "count_url_dots",
    "is_ip",
    "is_private",
    "is_filter",
    "num_port",
    "ratio_alpha_numeric",
    "value_entropy_url",
]


# ----------------------------------------------------------------------
# 2. DetectionResult — ML 탐지 모델팀 → AI·RAG 엔진팀
# ----------------------------------------------------------------------
@dataclass
class DetectionResult:
    """ml_detector.py의 출력 형식."""

    is_malicious: bool        # 정상(False) / 악성(True)
    confidence_score: float   # 악성일 확률 (0.0 ~ 1.0)

    def to_dict(self) -> dict:
        return asdict(self)


# ----------------------------------------------------------------------
# 3. AnalysisResult — AI·RAG 엔진팀 → 앱·통합팀(Streamlit)
# ----------------------------------------------------------------------
@dataclass
class AnalysisResult:
    """rag_engine.py의 출력 형식."""

    reason: str                              # 위험/안전 판단 사유
    countermeasures: List[str] = field(default_factory=list)  # 대응 지침 목록

    def to_dict(self) -> dict:
        return asdict(self)


# ----------------------------------------------------------------------
# 4. ScanReport — 최종 통합 결과 (app.py가 화면에 렌더링하는 최종 형식)
# ----------------------------------------------------------------------
@dataclass
class ScanReport:
    """5단계 파이프라인의 최종 결과물. Streamlit 화면은 이 객체 하나만 받아 렌더링합니다."""

    url: str
    features: FeatureVector
    detection: DetectionResult
    analysis: AnalysisResult

    def to_dict(self) -> dict:
        return {
            "url": self.url,
            "is_malicious": self.detection.is_malicious,
            "confidence_score": self.detection.confidence_score,
            "extracted_features": self.features.to_dict(),
            "ai_analysis": self.analysis.to_dict(),
        }