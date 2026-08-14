"""
    - 입력에 http://가 명시된 경우에는 HTTP 요청을 허용
    - 스킴이 없는 URL에서 HTTPS가 실패해도 HTTP로 자동 재시도하지 않음
    - localhost, 사설/예약 IP, 비표준 포트는 차단
    - url_resolver.py에서만 스킴 붙여 원본 url 추적 -> url_to_feature에서 스킴 삭제
"""

import ipaddress
import re
import socket
from urllib.parse import urljoin, urlsplit

import requests


_SUPPORTED_SCHEMES = frozenset({"http", "https"})
_STANDARD_PORTS = frozenset({80, 443})
_SCHEME_PREFIX_PATTERN = re.compile(r"^([A-Za-z][A-Za-z0-9+.-]*):")


class URLResolutionError(Exception):
    """URL 복구 과정에서 발생하는 예외입니다."""

    pass


def prepare_url(url):
    """외부 요청용 URL을 만들되 HTTP 자동 fallback은 수행하지 않습니다."""

    if not isinstance(url, str):
        raise URLResolutionError("URL은 문자열이어야 합니다.")

    url = url.strip()

    if not url:
        raise URLResolutionError("URL이 비어 있습니다.")

    # mailto:, javascript: 등의 명시적 비웹 스킴은 HTTPS 주소로 오인하지 않는다.
    scheme_prefix = _SCHEME_PREFIX_PATTERN.match(url)
    if scheme_prefix and "://" not in url:
        prefix = scheme_prefix.group(1).lower()
        # example.com:8080처럼 스킴 없는 host:port 형식은 아래에서 URL로 처리한다.
        if "." not in prefix and prefix != "localhost":
            raise URLResolutionError("HTTP 또는 HTTPS URL만 지원합니다.")

    # 스킴이 없다면 HTTPS만 사용하며 HTTP로 자동 재시도하지 않는다.
    if "://" not in url:
        url = f"https://{url}"

    parsed = urlsplit(url)

    if parsed.scheme.lower() not in _SUPPORTED_SCHEMES:
        raise URLResolutionError(
            "HTTP 또는 HTTPS URL만 지원합니다."
        )

    if not parsed.hostname:
        raise URLResolutionError(
            "도메인이 없는 URL입니다."
        )

    return url


def _validate_public_destination(url):
    """요청 목적지가 외부 공개 HTTP(S) 주소인지 검사합니다."""

    parsed = urlsplit(url)

    if parsed.scheme.lower() not in _SUPPORTED_SCHEMES:
        raise URLResolutionError("HTTP 또는 HTTPS URL만 지원합니다.")

    hostname = parsed.hostname
    if not hostname:
        raise URLResolutionError("도메인이 없는 URL입니다.")

    if parsed.username is not None or parsed.password is not None:
        raise URLResolutionError("사용자 정보가 포함된 URL은 지원하지 않습니다.")

    try:
        port = parsed.port
    except ValueError as error:
        raise URLResolutionError("올바르지 않은 포트 번호입니다.") from error

    if port is not None and port not in _STANDARD_PORTS:
        raise URLResolutionError("보안을 위해 80번과 443번 포트만 허용합니다.")

    try:
        ip_addresses = {
            item[4][0]
            for item in socket.getaddrinfo(
                hostname,
                port or (443 if parsed.scheme.lower() == "https" else 80),
                type=socket.SOCK_STREAM,
            )
        }
    except socket.gaierror as error:
        raise URLResolutionError("도메인의 IP 주소를 확인할 수 없습니다.") from error

    if not ip_addresses:
        raise URLResolutionError("도메인의 IP 주소를 확인할 수 없습니다.")

    for address in ip_addresses:
        try:
            ip = ipaddress.ip_address(address)
        except ValueError as error:
            raise URLResolutionError("올바르지 않은 IP 주소입니다.") from error

        # is_global이 아닌 주소에는 사설, loopback, link-local, reserved 등이 포함된다.
        if not ip.is_global:
            raise URLResolutionError(
                "localhost, 사설 IP 또는 예약 IP 주소에는 접근할 수 없습니다."
            )

    return parsed


def resolve_url(url, max_redirects=5):
    """각 목적지를 검사하며 리디렉션을 수동으로 추적합니다."""

    request_url = prepare_url(url)

    session = requests.Session()
    session.trust_env = False

    try:
        current_url = request_url

        for redirect_count in range(max_redirects + 1):
            current_parsed = _validate_public_destination(current_url)

            with session.get(
                current_url,
                allow_redirects=False,
                stream=True,
                timeout=(3, 5),
                headers={
                    "User-Agent": "Q-Shield-URL-Resolver/1.0"
                },
            ) as response:
                if not response.is_redirect and not response.is_permanent_redirect:
                    return response.url

                if redirect_count >= max_redirects:
                    raise URLResolutionError(
                        f"리디렉트가 {max_redirects}회를 초과했습니다."
                    )

                location = response.headers.get("Location")
                if not location:
                    raise URLResolutionError(
                        "리디렉션 응답에 목적지 URL이 없습니다."
                    )

                next_url = urljoin(current_url, location)
                next_parsed = urlsplit(next_url)

                # HTTPS에서 HTTP로 내려가는 리디렉션은 차단한다.
                if (
                    current_parsed.scheme.lower() == "https"
                    and next_parsed.scheme.lower() == "http"
                ):
                    raise URLResolutionError(
                        "HTTPS에서 HTTP로 전환되는 리디렉션은 차단했습니다."
                    )

                # 다음 반복에서 실제 요청 전에 스킴, 포트, IP를 다시 검사한다.
                current_url = next_url

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
