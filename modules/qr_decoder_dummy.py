from pathlib import Path


def extract_url_from_qr(image_path) -> str | None:
    """QR 디코딩 MOCK 함수. 실제로 QR을 읽지 않고, 파일 존재 여부만 확인 후 임의의 URL을 반환."""
    if not Path(image_path).exists():
        return None
    return "http://secure-login.paypa1.com/verify"
