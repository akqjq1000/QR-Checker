"""QR에서 디코딩한 URL 문자열의 16개 정적 피처를 추출하는 모듈.

이 파일의 계산식은 ``http://`` 또는 ``https://``가 없는 URL도 입력할 수
있으며, 이 경우 URL을 분리할 때만 임시로 ``http://``를 붙입니다. 피처는
원본 문자열을 기준으로 계산하므로 학습 데이터와 실제 QR 입력의 기준이
달라지지 않습니다.
"""

from __future__ import annotations

import math
import re
from typing import Final
from urllib.parse import ParseResult, urlparse

from modules.schema import *


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


def _validate_url_text(url: str) -> str:
    """URL 입력값을 검사하고 앞뒤 공백을 제거한 원본 문자열을 반환한다."""

    if not isinstance(url, str):
        raise TypeError("url은 문자열(str)이어야 합니다.")

    cleaned_url = url.strip()
    if not cleaned_url:
        raise ValueError("url이 비어 있습니다.")

    if any(character.isspace() for character in cleaned_url):
        raise ValueError("url에는 공백 문자를 포함할 수 없습니다.")

    # ftp://, mailto:// 등 HTTP(S)가 아닌 명시적 프로토콜은 분석하지 않는다.
    scheme_match = _SCHEME_PATTERN.match(cleaned_url)
    if scheme_match:
        scheme = cleaned_url.split(":", 1)[0].lower()
        if scheme not in _HTTP_SCHEMES:
            raise ValueError("http:// 또는 https:// URL만 지원합니다.")

    return cleaned_url


def _parse_url(cleaned_url: str) -> tuple[ParseResult, str, str, str, int]:
    """학습 전처리와 같은 방식으로 URL을 domain, path, query, port로 나눈다."""

    # 프로토콜이 없는 QR URL은 파싱할 때만 임시 프로토콜을 사용
    parse_target = cleaned_url
    if not cleaned_url.lower().startswith(("http://", "https://")):
        parse_target = f"http://{cleaned_url}"

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
        parsed = urlparse(f"http://{domain}{path}")

    if not domain:
        raise ValueError("URL에 도메인 또는 IP 주소가 없습니다.")

    return parsed, domain, path, query, port


def _split_domain(domain: str) -> tuple[str, str, str]:
    """단순 점 분리 방식으로 도메인을 나눈다."""

    parts = domain.split(".")

    if len(parts) > 2:
        return ".".join(parts[:-2]), parts[-2], parts[-1]
    if len(parts) == 2:
        return "", parts[0], parts[1]
    return "", domain, ""


def _calculate_entropy(text: str) -> float:
    """URL 문자열의 Shannon entropy를 계산한다."""

    if not text:
        return 0.0

    length = len(text)
    entropy = 0.0

    # ML팀 preprocess_data.py와 연산 순서까지 동일하게 계산합니다.
    for character in set(text):
        probability = text.count(character) / length
        entropy += -probability * math.log(probability, 2)

    return float(entropy)


def extract_features(url: str) -> FeatureVector:
    """URL 하나를 받아 ML 학습 기준의 16개 피처를 반환한다.

    프로토콜이 없는 ``example.com/path`` 형식도 지원. 프로토콜은
    파싱용으로만 임시 추가되며, 모든 문자열 기반 피처는 입력 원문을 기준으로
    계산.
    """

    cleaned_url = _validate_url_text(url)
    _, domain, path, query, port = _parse_url(cleaned_url)
    sub_domain, root_domain, suffix = _split_domain(domain)

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

''' 테스트'''
if __name__ == "__main__":
    sample_url = "g00gle-login.com:8080/verify?id=123"
    sample_features = extract_features(sample_url)

    print("입력 URL:", sample_url)
    print("피처 딕셔너리:", sample_features.to_dict())
    print("ML 입력 배열:", sample_features.to_array())
