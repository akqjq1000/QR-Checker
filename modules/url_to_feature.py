"""피처 추출 모듈.
입력 URL에 ``http://`` 또는 ``https://``가 있으면 ML 피처 계산 직전에
제거. URL을 분리할 때만 임시로 ``//``를 붙여 도메인의 시작 위치를
알려주며, 프로토콜을 제외한 학습 데이터와 실제 QR 입력의 기준을 맞춤.
"""

from __future__ import annotations

import math
import re
from typing import Final
from urllib.parse import ParseResult, urlparse

import tldextract

from .schema import *


_HTTP_SCHEMES: Final[frozenset[str]] = frozenset({"http", "https"})
_SCHEME_PATTERN: Final = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*://")
_ENCODING_PATTERN: Final = re.compile(r"%[0-9A-Fa-f]{2}")
_ASCII_ALNUM_PATTERN: Final = re.compile(r"[A-Za-z0-9]")
_IPV4_PATTERN: Final = re.compile(r"^\d{1,3}(?:\.\d{1,3}){3}$")

_FILTER_WORDS: Final[tuple[str, ...]] = (
    "login",
    "verify",
    "bank",
    "secure",
    "account",
    "update",
)


def normalize_url_for_features(url: str) -> str:
    """ML 피처 계산용 URL에서 HTTP/HTTPS 프로토콜을 제거."""

    if not isinstance(url, str):
        raise TypeError("url은 문자열(str)이어야 합니다.")

    normalized_url = url.strip()
    if not normalized_url:
        raise ValueError("url이 비어 있습니다.")

    if any(character.isspace() for character in normalized_url):
        raise ValueError("url에는 공백 문자를 포함할 수 없습니다.")

    scheme_match = _SCHEME_PATTERN.match(normalized_url)
    if scheme_match:
        scheme = normalized_url.split(":", 1)[0].lower()
        if scheme not in _HTTP_SCHEMES:
            raise ValueError("http:// 또는 https:// URL만 지원합니다.")

    return re.sub(
        r"^https?://",
        "",
        normalized_url,
        count=1,
        flags=re.IGNORECASE,
    )


def _validate_url_text(url: str) -> str:
    return normalize_url_for_features(url)


def _parse_url(cleaned_url: str) -> tuple[ParseResult, str, str, str, int]:
    """학습 전처리와 같은 방식으로 URL을 domain, path, query, port로 나눈다."""

    # urlparse가 첫 부분을 경로가 아닌 도메인으로 인식하도록 파싱할 때만
    # 임시로 //를 붙인다. cleaned_url 자체와 ML 피처에는 //가 포함되지 않는다.
    parse_target = f"//{cleaned_url}"

    try:
        parsed = urlparse(parse_target)
        domain = parsed.netloc
        path = parsed.path
        query = parsed.query

        try:
            port = parsed.port if parsed.port else -1
        except ValueError:
            port = -1
    except ValueError:
        # 문자열을 기준으로 분리합니다.
        clean_target = re.sub(r"^https?://", "", cleaned_url, flags=re.IGNORECASE)
        domain = clean_target.split("/", 1)[0]
        path = f"/{clean_target.split('/', 1)[1]}" if "/" in clean_target else ""
        query = ""
        port = -1
        parsed = urlparse(f"//{domain}{path}")

    if not domain:
        raise ValueError("URL에 도메인 또는 IP 주소가 없습니다.")

    return parsed, domain, path, query, port


def split_domain(domain: str) -> tuple[str, str, str]:
    """tldextract(Public Suffix List) 기반으로 domain을 (subdomain, root_domain, suffix)로 나눈다.

    기존에는 단순 점(.) 분리였으나, wikipedia.co.kr처럼 복합 suffix를
    가진 도메인을 잘못 자르는 문제가 있어 tldextract로 교체함.
    domain_similarity.py의 화이트리스트 매칭도 이 함수를 그대로 재사용해서
    root domain 계산 기준을 프로젝트 전체에서 하나로 통일한다.
    """
    ext = tldextract.extract(domain)

    if not ext.domain:
        # tldextract가 인식 못한 경우(순수 IP 등) 폴백
        parts = domain.split(".")
        if len(parts) > 2:
            return ".".join(parts[:-2]), parts[-2], parts[-1]
        if len(parts) == 2:
            return "", parts[0], parts[1]
        return "", domain, ""

    return ext.subdomain, ext.domain, ext.suffix


# 기존 내부 호출부 및 하위 호환용 별칭
_split_domain = split_domain


def _calculate_entropy(text: str) -> float:
    """URL 문자열의 Shannon entropy를 계산."""

    if not text:
        return 0.0

    length = len(text)
    entropy = 0.0

    for character in set(text):
        probability = text.count(character) / length
        entropy += -probability * math.log(probability, 2)

    return float(entropy)


def extract_features(url: str) -> FeatureVector:
    """URL 하나를 받아 ML 학습 기준의 17개 피처를 반환.

    프로토콜이 있는 URL과 없는 URL을 모두 지원하며, HTTP/HTTPS 프로토콜은
    제거한 뒤 모든 문자열 기반 피처를 계산.
    """

    cleaned_url = _validate_url_text(url)
    _, domain, path, query, port = _parse_url(cleaned_url)
    sub_domain, root_domain, suffix = split_domain(domain)

    is_ip = bool(_IPV4_PATTERN.fullmatch(domain.split(":", 1)[0]))
    is_private = bool(
        is_ip
        and domain.startswith(("192.168.", "10.", "172."))
    )

    alnum_count = len(_ASCII_ALNUM_PATTERN.findall(cleaned_url))

    features = FeatureVector(
        len_url=len(cleaned_url),
        len_sub_domain=len(sub_domain),
        len_root_domain=len(root_domain),
        len_suffix=len(suffix),
        len_encoding=len(_ENCODING_PATTERN.findall(cleaned_url)) * 3,
        len_query=len(query),
        count_sub_domain=len(sub_domain.split(".")) if sub_domain else 0,
        count_file_path=path.count("/"),
        count_special_char=len(re.findall(r"[^A-Za-z0-9]", cleaned_url)),
        count_url_dots=cleaned_url.count("."),
        is_ip=is_ip,
        is_private=is_private,
        is_filter=any(word in cleaned_url.lower() for word in _FILTER_WORDS),
        num_port=port,
        ratio_alpha_numeric=(
            alnum_count / len(cleaned_url) if cleaned_url else 0.0
        ),
        value_entropy_url=_calculate_entropy(cleaned_url),
    )

    if list(features.to_dict()) != FEATURE_ORDER:
        raise RuntimeError(
            "FeatureVector의 필드 순서가 FEATURE_ORDER와 일치하지 않습니다."
        )

    return features


extract = extract_features

'''테스트'''
if __name__ == "__main__":
    sample_url = "g00gle-login.com:8080/verify?id=123"
    sample_features = extract_features(sample_url)

    print("입력 URL:", sample_url)
    print("피처 딕셔너리:", sample_features.to_dict())
    print("ML 입력 배열:", sample_features.to_array())