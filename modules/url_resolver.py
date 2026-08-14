"""
QR에서 추출된 URL의 리디렉트를 따라가 
최종 목적지 URL을 반환하는 모듈.
request 설치 필요
처리 흐름:
    QR 디코딩 URL
    → URL 형식 검사
    → 스킴 없으면 https/http 후보 생성
    → 리디렉트 추적 (후보 순차 시도, 연결 실패 시에만 폴백)
    → 최종 URL 반환
    → URL 피처 추출 모듈에 전달
"""
from urllib.parse import urlsplit
import requests

class URLResolutionError(Exception):
    """URL 복구 과정에서 발생하는 예외입니다."""
    pass

def _validate_string(url):
    """URL이 유효한 문자열인지 검사합니다."""
    if not isinstance(url, str):
        raise URLResolutionError("URL은 문자열이어야 합니다.")
    url = url.strip()
    if not url:
        raise URLResolutionError("URL이 비어 있습니다.")
    return url

def _build_candidates(url):
    """
    요청에 사용할 URL 후보 목록을 생성합니다.
    - 스킴이 이미 있으면 http/https만 허용하고 그대로 사용
    - 스킴이 없으면 https, http 순서로 후보를 만들어
      순차적으로 시도 (https 고정 강제 X, 완전 제거도 X)
    """
    if "://" in url:
        parsed = urlsplit(url)
        if parsed.scheme.lower() not in {"http", "https"}:
            raise URLResolutionError("HTTP 또는 HTTPS URL만 지원합니다.")
        if not parsed.hostname:
            raise URLResolutionError("도메인이 없는 URL입니다.")
        return [url]

    candidates = [f"https://{url}", f"http://{url}"]
    for candidate in candidates:
        parsed = urlsplit(candidate)
        if not parsed.hostname:
            raise URLResolutionError("도메인이 없는 URL입니다.")
    return candidates

def resolve_url(url, max_redirects=5):
    """
    리디렉트를 추적하여 최종 목적지 URL 문자열을 반환합니다.
    스킴이 없는 URL은 https를 먼저 시도하고,
    연결 자체가 실패하면 http로 재시도합니다.
    """
    url = _validate_string(url)
    candidates = _build_candidates(url)

    session = requests.Session()
    session.max_redirects = max_redirects
    session.trust_env = False

    last_error = None
    try:
        for candidate in candidates:
            try:
                with session.get(
                    candidate,
                    allow_redirects=True,
                    stream=True,
                    timeout=(3, 5),
                    headers={
                        "User-Agent": "Q-Shield-URL-Resolver/1.0"
                    },
                ) as response:
                    return response.url

            except requests.TooManyRedirects as error:
                # 스킴 문제가 아니므로 바로 실패 처리1
                raise URLResolutionError(
                    f"리디렉트가 {max_redirects}회를 초과했습니다."
                ) from error

            except requests.Timeout as error:
                # 스킴 문제가 아니므로 바로 실패 처리2
                raise URLResolutionError(
                    "URL 확인 시간이 초과되었습니다."
                ) from error

            except requests.ConnectionError as error:
                # https 연결 자체가 안 되는 경우(SSL 미지원 등)만
                # 다음 후보(http)로 넘어가서 재시도
                last_error = URLResolutionError(
                    f"URL 요청에 실패했습니다: {error}"
                )
                continue

            except requests.RequestException as error:
                raise URLResolutionError(
                    f"URL 요청에 실패했습니다: {error}"
                ) from error

        # 모든 후보가 ConnectionError로 실패한 경우
        raise last_error
    finally:
        session.close()

# ==========================================
# 테스트
# ==========================================
if __name__ == "__main__":
    test_cases = [
        "https://tinyurl.com/ynphet7f",  # 원본: https://www.naver.com
        "tinyurl.com/ynphet7f",          # 스킴 없는 케이스
    ]
    for url in test_cases:
        try:
            original_url = resolve_url(url)
            print("입력 URL:", url)
            print("원본 URL:", original_url)
        except URLResolutionError as e:
            print("입력 URL:", url)
            print("복구 실패:", e)