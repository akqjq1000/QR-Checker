"""
[단축 URL 원본 복구 모듈]
단축 URL(bit.ly, tinyurl 등) → 리다이렉트를 따라가 최종 원본 URL 추출

[사용 라이브러리]
requests: HTTP 요청 및 리다이렉트 자동 추적

[함수 설명]
get_original_url(url)
  - 입력: 단축 URL 문자열
  - 출력: 리다이렉트를 모두 따라간 최종 원본 URL (실패 시 None)
  - 동작 방식: 단축 서비스는 접속 시 실제 내용 대신 "301/302 + Location
    헤더(진짜 주소)"만 응답함. allow_redirects=True로 requests가 이
    과정을 최종 200 응답이 나올 때까지 자동 반복 추적 -> response.url이
    최종 도착 주소
  - HEAD 요청 사용 이유: 최종 주소만 필요하고 페이지 내용은 필요 없으므로
    GET보다 가벼운 HEAD로 요청
  - timeout=10: 응답 없는 서버에 무한 대기 방지
  - 예외 처리: 서버 무응답/존재하지 않는 도메인 등 어떤 오류든 None 반환
    (파이프라인 규칙: 복구 실패 시 원래 단축 URL 그대로 사용)

[결과]
1) 직접 만든 단축 URL  -> 원본 URL 정상 반환
2) 이미 원본인 URL  -> 입력과 동일하게 반환
3) 존재하지 않는 도메인  -> None 반환
4) URL 형식이 아닌 문자열  -> None 반환
"""
import requests

def get_original_url(url):
    try:
        response = requests.head(
            url,
            allow_redirects=True,
            timeout=10
        )

        return response.url

    except requests.RequestException:
        return None

# 테스트
url = "https://zrr.kr/YiWTEb"  # 확인할 본인 url로 변경
original_url = get_original_url(url)
print("원본 URL:", original_url)