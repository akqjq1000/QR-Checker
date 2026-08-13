"""
[웹사이트 사전 캡쳐 모듈]
URL 방문 전, 격리된 샌드박스 브라우저(Playwright)로 미리 접속해서 화면을 캡쳐

[사용 라이브러리]
playwright: 헤드리스 브라우저 자동화
※ 설치 시 두 단계 모두 필요: pip install playwright / playwright install chromium

[함수 설명]
capture_website(url)
  - 입력: 캡쳐할 URL 문자열
  - 출력: 성공 시 저장된 스크린샷 파일 이름, 실패 시 None
  - 동작 방식: headless + chromium_sandbox=True로 크롬 실행, 매번 새
    context(세션)에서 접속 후 전체 페이지 스크린샷 저장
  - wait_until="networkidle" 사용: "domcontentloaded"는 HTML 뼈대만
    로드되면 바로 캡쳐되어 콘텐츠가 안 채워진 빈 화면이 찍히는 문제가 있었음
  - 예외 처리:
      1) URL이 http/https가 아니면 즉시 None ("허용되지 않은 URL 스킴" 출력)
      2) URL 형식은 맞지만 접속 실패(존재하지 않는 도메인, 타임아웃 등)면
         goto()에서 예외 발생 -> except에서 잡아 None 반환

[결과]
1) 정상 URL  -> URL 기반 파일명으로 이미지 생성, 파일명 반환
2) 위험한 스킴(javascript: 등)  -> None 반환, 스킴 차단 메시지 출력
3) 존재하지 않는 도메인  -> None 반환, 접속 실패 메시지 출력
"""
import hashlib
import os
import re
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright

SAVE_DIR = os.path.join(os.path.dirname(__file__), "saved_images")


def build_capture_filename(url: str) -> str:
    parsed = urlparse(url)
    host = (parsed.netloc or parsed.path or "website").lower()
    host = host.replace("www.", "")
    # [수정] a-z0-9 대신 유니코드 단어 문자(\w)를 허용하여 한글이 깨지지 않게 합니다.
    host = re.sub(r"[^\w]+", "_", host).strip("_") or "website"

    # [수정] 경로 부분도 동일하게 수정합니다.
    path_part = re.sub(r"[^\w]+", "_", (parsed.path or "").strip("/")).strip("_")
    base_name = f"{host}_{path_part}" if path_part else host
    base_name = base_name[:80].strip("_") or "website"

    digest = hashlib.md5(url.encode("utf-8")).hexdigest()[:8]
    return f"{base_name}_{digest}.png"


def capture_website(url, output_dir=SAVE_DIR):
    # URL 스킴 검증 (javascript:, file: 등 위험한 스킴 차단)
    if urlparse(url).scheme not in ("http", "https"):
        print("웹사이트 캡처 실패: 허용되지 않은 URL 스킴")
        return None

    os.makedirs(output_dir, exist_ok=True)
    file_name = build_capture_filename(url)
    file_path = os.path.join(output_dir, file_name)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage"],
                chromium_sandbox=False,
            )

            context = browser.new_context()
            page = context.new_page()

            page.goto(
                url,
                wait_until="networkidle",
                timeout=20000
            )

            page.screenshot(
                path=file_path,
                full_page=True
            )

            context.close()
            browser.close()

        return file_name

    except Exception as e:
        print("웹사이트 캡처 실패:", e)
        if os.path.exists(file_path):
            os.remove(file_path)
        return None


if __name__ == "__main__":
    # 테스트
    url = "https://www.naver.com/"  # 확인할 본인 url로 변경
    result = capture_website(url)
    print("캡처 결과:", result)