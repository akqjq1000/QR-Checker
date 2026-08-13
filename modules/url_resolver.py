"""
QR에서 추출된 URL의 리디렉트를 따라가 
최종 목적지 URL을 반환하는 모듈.
request 설치 필요

처리 흐름:
    QR 디코딩 URL
    → URL 형식 검사
    → 프로토콜이 없으면 HTTPS 추가
    → 리디렉트 추적
    → 최종 URL 반환
    → URL 피처 추출 모듈에 전달
"""

from urllib.parse import urlsplit

import requests


class URLResolutionError(Exception):
    """URL 복구 과정에서 발생하는 예외입니다."""

    pass


def prepare_url(url):
    """외부 요청에 사용할 수 있도록 URL을 검사하고 정리합니다."""

    if not isinstance(url, str):
        raise URLResolutionError("URL은 문자열이어야 합니다.")

    url = url.strip()

    if not url:
        raise URLResolutionError("URL이 비어 있습니다.")

    # 프로토콜이 없다면 HTTPS를 우선 사용
    if "://" not in url:
        url = f"https://{url}"

    parsed = urlsplit(url)

    if parsed.scheme.lower() not in {"http", "https"}:
        raise URLResolutionError(
            "HTTP 또는 HTTPS URL만 지원합니다."
        )

    if not parsed.hostname:
        raise URLResolutionError(
            "도메인이 없는 URL입니다."
        )

    return url


def resolve_url(url, max_redirects=5):
    """리디렉트를 추적하여 최종 목적지 URL 문자열을 반환합니다."""

    request_url = prepare_url(url)

    session = requests.Session()
    session.max_redirects = max_redirects
    session.trust_env = False

    try:
        with session.get(
            request_url,
            allow_redirects=True,
            stream=True,
            timeout=(3, 5),
            headers={
                "User-Agent": "Q-Shield-URL-Resolver/1.0"
            },
        ) as response:

            return response.url

    except requests.TooManyRedirects as error:
        raise URLResolutionError(
            f"리디렉트가 {max_redirects}회를 초과했습니다."
        ) from error

    except requests.Timeout as error:
        raise URLResolutionError(
            "URL 확인 시간이 초과되었습니다."
        ) from error

    except requests.RequestException as error:
        raise URLResolutionError(
            f"URL 요청에 실패했습니다: {error}"
        ) from error

    finally:
        session.close()


# ==========================================
# 테스트
# ==========================================

if __name__ == "__main__":
    url = "https://tinyurl.com/ynphet7f"  # 테스트 URL로 변경(원본:https://www.naver.com )

    original_url = resolve_url(url)

    print("입력 URL:", url)
    print("원본 URL:", original_url)
