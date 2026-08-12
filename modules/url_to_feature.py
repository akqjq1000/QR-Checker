"""QR 코드에서 디코딩된 URL의 16개 정적 피처를 추출하는 모듈.
# 외부 라이브러리 tldextract>=5.3,<6 설치 필요!

전체 처리 흐름
-------------
1. QR 디코딩 모듈이 URL 문자열을 추출한다.
2. 이 모듈의 ``extract_features(url)`` 함수가 URL을 검증하고 분석한다.
3. 계산한 16개 피처를 ``schema.py``의 ``FeatureVector`` 객체로 반환한다.
4. ML 모델은 ``FeatureVector.to_array()``로 고정 순서의 값을 전달받는다.

이 모듈은 QR 이미지 자체를 읽지 않는다. QR에서 이미 디코딩된
``http://`` 또는 ``https://`` URL 문자열만 입력받는다.
"""

from __future__ import annotations

import ipaddress              # 문자열이 IPv4/IPv6 주소인지 판별
import math                   # Shannon entropy 계산에 log2 사용
import re                     # URL 인코딩·알파벳·숫자 패턴 탐색
from collections import Counter  # URL에 등장한 각 문자의 빈도 계산
from typing import Final      # 실행 중 바꾸지 않을 상수임을 표시
from urllib.parse import SplitResult, urlsplit  # URL 구성 요소 분리

# 팀 공통 데이터 형식과 ML 입력 피처 순서를 schema.py에서 가져옵니다.
# feature_extractor.py 안에 별도의 결과 형식을 다시 정의하지 않습니다.
from schema import FEATURE_ORDER, FeatureVector

try:
    import tldextract
except ImportError as exc:  # 실행 환경에 라이브러리가 없을 때 원인을 명확히 안내
    raise ImportError(
        "tldextract가 필요합니다. 'pip install tldextract'로 설치하세요."
    ) from exc


# 도메인을 서브도메인·등록 도메인·suffix로 정확하게 분리하는 도구입니다.
# suffix_list_urls=(): 실행할 때 인터넷에서 최신 PSL을 받지 않습니다.
# cache_dir=None: 별도의 PSL 캐시 파일을 만들거나 사용하지 않습니다.
# include_psl_private_domains=True: github.io, blogspot.com 같은
# Private Suffix도 일반 Public Suffix와 구분해 분석합니다.
_DOMAIN_EXTRACTOR: Final = tldextract.TLDExtract(
    suffix_list_urls=(),
    cache_dir=None,
    include_psl_private_domains=True,   # private TLD(suffix) 판별 활성롸
)

# count_special_char 계산에 사용할 특수문자 목록입니다.
# 이 목록은 ML 학습 데이터와 실제 추론 코드에서 반드시 동일해야 합니다.
# 현재 '.'은 count_url_dots에서도 별도로 계산되므로 두 피처에 중복 반영됩니다.
# 중복 포함 여부와 최종 문자 목록은 QR·피처팀과 ML팀이 함께 확정해야 합니다.
_SPECIAL_CHARACTERS: Final[frozenset[str]] = frozenset("?=-@%.")

# is_filter 계산에 사용할 피싱 참고 단어 목록입니다.
# 한 단어라도 포함되면 is_filter=True가 되지만, 그 자체로 악성을 확정하지는 않습니다.
# 이 목록도 ML 학습과 실제 추론에서 같은 기준을 사용해야 합니다.
_FILTER_WORDS: Final[tuple[str, ...]] = (
    "login",
    "verify",
    "update",
    "bank",
    "account",
    "secure",
    "password",
    "payment",
)

# 반복해서 사용할 정규표현식을 미리 컴파일합니다.
# %XX: URL 퍼센트 인코딩 한 단위(예: %20, %2F)
_ENCODING_PATTERN: Final = re.compile(r"%[0-9A-Fa-f]{2}")
_ASCII_ALPHA_PATTERN: Final = re.compile(r"[A-Za-z]")  # 영문 알파벳
_DIGIT_PATTERN: Final = re.compile(r"[0-9]")           # 숫자


def _parse_http_url(url: str) -> tuple[str, SplitResult, str, int]:
    """URL을 검증하고 정리된 URL, 파싱 결과, 호스트명, 포트를 반환한다.

    함수 이름 앞의 ``_``는 이 모듈 내부에서만 사용하는 보조 함수라는 뜻입니다.
    잘못된 입력은 그대로 계산하지 않고 TypeError 또는 ValueError로 알려줍니다.
    """

    # URL이 문자열인지 먼저 확인합니다.
    if not isinstance(url, str):
        raise TypeError("url은 문자열(str)이어야 합니다.")

    # 복사 과정에서 앞뒤에 들어간 불필요한 공백은 제거합니다.
    cleaned_url = url.strip()
    if not cleaned_url:
        raise ValueError("url이 비어 있습니다.")

    # URL 중간의 공백은 주소 형식 오류로 처리합니다.
    if any(character.isspace() for character in cleaned_url):
        raise ValueError("url에는 공백 문자를 포함할 수 없습니다.")

    # URL을 scheme, netloc, path, query, fragment 등으로 나눕니다.
    parsed = urlsplit(cleaned_url)
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("http:// 또는 https://로 시작하는 URL만 지원합니다.")

    # parsed.port는 잘못된 포트(예: :abc, :99999)에서 ValueError를 발생시킵니다.
    try:
        hostname = parsed.hostname
        explicit_port = parsed.port
    except ValueError as exc:
        raise ValueError("URL의 호스트명 또는 포트 번호 형식이 올바르지 않습니다.") from exc

    if not hostname:
        raise ValueError("URL에 도메인 또는 IP 주소가 없습니다.")

    # 포트가 URL에 직접 적혀 있지 않으면 schema.py 기준에 따라 -1을 사용합니다.
    port = explicit_port if explicit_port is not None else -1

    # 도메인 비교가 일정하도록 소문자로 바꾸고 마지막의 불필요한 점을 제거합니다.
    return cleaned_url, parsed, hostname.lower().rstrip("."), port


def _is_ip_address(hostname: str) -> bool:
    """호스트명이 IPv4 또는 IPv6 주소이면 True를 반환한다."""

    # ipaddress가 정상적으로 해석하면 IP이고, 실패하면 일반 도메인입니다.
    try:
        ipaddress.ip_address(hostname)
        return True
    except ValueError:
        return False


def _calculate_entropy(text: str) -> float:
    """문자 분포를 이용해 문자열의 Shannon entropy를 계산한다.

    같은 문자가 반복되는 단순한 문자열은 엔트로피가 낮아지고,
    여러 문자가 다양하게 등장하는 복잡한 문자열은 엔트로피가 높아집니다.
    """
    text_length = len(text)
    if text_length == 0:
        return 0.0

    # 각 문자의 등장 확률 p에 대해 -Σ(p * log2(p))를 계산합니다.
    return -sum(
        (count / text_length) * math.log2(count / text_length)
        for count in Counter(text).values()
    )


def extract_features(url: str) -> FeatureVector:
    """HTTP(S) URL 하나를 받아 16개 피처를 FeatureVector로 반환한다.

    계산 기준:
    - len_root_domain: 포트 번호를 제외한 전체 호스트명의 길이
    - len_suffix: 등록 가능 도메인(SLD + public/private suffix)의 길이
    - len_encoding: ``%XX`` 형식으로 인코딩된 부분의 총 문자 길이
    - count_file_path: URL path에 포함된 ``/`` 개수
    - ratio_alpha_numeric: 숫자 개수 / 영문 알파벳 개수
    """
    # 1단계: 입력 URL을 검증하고 구성 요소로 분리합니다.
    cleaned_url, parsed, hostname, port = _parse_http_url(url)

    # 2단계: 호스트가 일반 도메인인지 IP 주소인지 확인합니다.
    ip_address_used = _is_ip_address(hostname)

    if ip_address_used:
        # IP 주소에는 서브도메인과 Private Suffix 개념을 적용하지 않습니다.
        subdomain = ""
        registered_domain = hostname
        private_suffix_used = False
    else:
        # 예: shop.example.co.kr
        # subdomain='shop', domain='example', suffix='co.kr' 형태로 분석합니다.
        domain_parts = _DOMAIN_EXTRACTOR(hostname)
        subdomain = domain_parts.subdomain

        # SLD와 suffix를 결합한 등록 가능 도메인입니다. 예: example.co.kr
        registered_domain = domain_parts.top_domain_under_public_suffix
        private_suffix_used = domain_parts.is_private

    # 3단계: 알파벳 대비 숫자 비율을 계산합니다.
    # 예: 알파벳 20개, 숫자 5개라면 5 / 20 = 0.25입니다.
    alphabet_count = len(_ASCII_ALPHA_PATTERN.findall(cleaned_url))
    digit_count = len(_DIGIT_PATTERN.findall(cleaned_url))

    # 알파벳이 하나도 없으면 0으로 나누는 오류를 막기 위해 0.0을 사용합니다.
    alpha_numeric_ratio = digit_count / alphabet_count if alphabet_count else 0.0

    # 4단계: 계산 결과를 schema.py의 FeatureVector 형식에 맞춰 저장합니다.
    # 아래 필드 순서는 schema.py의 FEATURE_ORDER와 동일하게 유지합니다.
    features = FeatureVector(
        # --- 길이 관련 피처 ---
        len_url=len(cleaned_url),
        len_sub_domain=len(subdomain),
        len_root_domain=len(hostname),
        len_suffix=len(registered_domain),

        # %20처럼 3글자로 이루어진 인코딩 단위의 전체 문자 길이를 더합니다.
        len_encoding=sum(
            len(match.group()) for match in _ENCODING_PATTERN.finditer(cleaned_url)
        ),
        len_query=len(parsed.query),

        # --- 개수 관련 피처 ---
        # 서브도메인이 a.b라면 점으로 나눈 결과가 2개이므로 2를 반환합니다.
        count_sub_domain=len(subdomain.split(".")) if subdomain else 0,

        # path 안의 '/' 개수를 경로 깊이 기준으로 사용합니다.
        count_file_path=parsed.path.count("/"),
        count_special_char=sum(
            character in _SPECIAL_CHARACTERS for character in cleaned_url
        ),
        count_url_dots=cleaned_url.count("."),

        # --- 구조적 피처 ---
        is_ip=ip_address_used,
        is_private=private_suffix_used,

        # 대소문자 차이 없이 필터 단어가 하나라도 포함되는지 확인합니다.
        is_filter=any(word in cleaned_url.lower() for word in _FILTER_WORDS),
        num_port=port,

        # --- 비율·복잡도 피처 ---
        # 결과가 너무 길어지지 않도록 소수점 여섯 자리로 정리합니다.
        ratio_alpha_numeric=round(alpha_numeric_ratio, 6),
        value_entropy_url=round(_calculate_entropy(cleaned_url), 6),
    )

    # 5단계: schema.py와 피처 순서가 달라졌는지 마지막으로 검사합니다.
    # 순서가 다르면 ML 학습 때와 예측 때 열이 뒤바뀔 수 있으므로 즉시 중단합니다.
    if list(features.to_dict()) != FEATURE_ORDER:
        raise RuntimeError("FeatureVector의 필드 순서가 FEATURE_ORDER와 일치하지 않습니다.")

    # 일반 딕셔너리가 아니라 schema.py의 FeatureVector 객체를 반환합니다.
    return features


# 기존 코드에서 extract(url)이라는 이름으로 호출하는 경우도 지원하는 별칭입니다.
# 두 이름은 같은 함수를 가리킵니다.
extract = extract_features


# 이 파일을 직접 실행했을 때만 동작하는 간단한 사용 예시입니다.
# 다른 파일에서 import할 때는 아래 코드가 자동 실행되지 않습니다.
if __name__ == "__main__":
    sample_url = "http://g00gle-login.com:8080/verify?id=123"
    sample_features = extract_features(sample_url)

    print("입력 URL:", sample_url)
    print("피처 딕셔너리:", sample_features.to_dict())
    print("ML 입력 배열:", sample_features.to_array())
