"""
[QR 디코딩 모듈]
QR 코드 이미지 → URL 문자열 추출

[사용 라이브러리]
- opencv-python (cv2): 이미지 파일을 읽고 전처리(흑백 변환, 이진화, 확대)
- pyzbar: 이미지에서 QR 코드를 실제로 읽어내는 라이브러리
  ※ 설치 시 파이썬 패키지(pip install pyzbar) 외에
    시스템에 zbar 프로그램이 별도로 필요할 수 있음
    (Windows는 Visual C++ Redistributable 설치 필요한 경우 있음)

[함수 설명]
extract_url_from_qr(image_path)
  - 입력: 이미지 파일 경로 (문자열, 예: "C:/images/qr.png")
  - 출력: QR 안에 담긴 URL 문자열 (인식 실패 또는 웹 URL로 볼 수 없는 경우 None)
  - 동작 방식: 한 번에 안 읽히는 QR(흐림/회전/저해상도 등)을 대비해 4단계로 재시도
      1) 원본 이미지 그대로 시도
      2) 흑백 변환 후 시도
      3) 이진화(threshold) 후 시도
      4) 이미지가 너무 작으면(300px 미만) 확대 후 시도
  - 예외 처리:
      1) QR을 못 읽은 경우 → None + 경고 출력
      2) http/https가 아닌 스킴인 경우 (ftp://, tel:, mailto: 등 ://  유무와 상관없이 콜론 기반 스킴 전부 포함) → None + 경고 출력
      3) 스킴이 아예 없는데 도메인 형태로도 볼 수 없는 경우
      * 스킴이 없고 도메인 형태(naver.com 등)인 경우만 통과
"""
import re
import cv2
from pyzbar.pyzbar import decode

# 콜론 기반 스킴 전체를 판별하기 위한 패턴
_ANY_SCHEME_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
_HTTP_SCHEMES = ("http://", "https://")

def read_qr(image):
    decoded_objects = decode(image)
    if decoded_objects:
        return decoded_objects[0].data.decode("utf-8")
    return None

def extract_url_from_qr(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print(f" 이미지를 불러올 수 없습니다: {image_path}")
        return None

    candidates = [image]
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    candidates.append(gray)

    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    candidates.append(binary)

    height, width = gray.shape
    if height < 300 or width < 300:
        scale = 300 / min(height, width)
        resized = cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
        candidates.append(resized)

    result_url = None
    for img in candidates:
        result_url = read_qr(img)
        if result_url:
            break

    # 예외 케이스 1: QR 자체를 아예 못 읽은 경우
    if result_url is None:
        print(f" QR 코드를 인식하지 못했습니다: {image_path}")
        return None

    # 예외 케이스 2: 콜론 기반 스킴이 있는데 http/https가 아닌 경우 거부
    scheme_match = _ANY_SCHEME_PATTERN.match(result_url)
    if scheme_match and not result_url.lower().startswith(_HTTP_SCHEMES):
        print(f" http/https 이외의 스킴은 지원하지 않습니다: {result_url}")
        return None

    # 예외 케이스 3: 스킴이 없는 경우, 최소한 도메인 형태인지 확인
    if not scheme_match:
        first_segment = result_url.split("/", 1)[0].split(":", 1)[0]
        if "." not in first_segment or ";" in result_url or " " in result_url:
            print(f" 도메인 형식이 아닌 QR 데이터입니다: {result_url}")
            return None

    return result_url


# 테스트
if __name__ == "__main__":
    image_path = r"테스트할_이미지_경로"  # 확인할 본인 QR 이미지 경로로 변경
    url = extract_url_from_qr(image_path)
    print(url)