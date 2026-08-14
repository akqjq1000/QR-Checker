from functools import lru_cache
from pathlib import Path

from rapidfuzz import fuzz, process

BASE_DIR = Path(__file__).resolve().parent.parent
WHITELIST_PATH = BASE_DIR / "data" / "whitelist.txt"


@lru_cache(maxsize=1)
def load_whitelist() -> set:
    with open(WHITELIST_PATH, encoding="utf-8") as f:
        return {line.strip() for line in f if line.strip()}


# 스킴이 있는 URL이 오면 안 됨
def extract_root_domain(url_or_domain: str) -> str:
    """url_to_feature.split_domain을 재사용해 root domain(root+suffix)을 구한다.

    순환 참조 방지를 위해 함수 내부에서 지연 임포트한다
    (url_to_feature.py도 이 모듈을 import하기 때문).
    """
    from .url_to_feature import split_domain

    domain = url_or_domain.split("/", 1)[0].split(":", 1)[0]
    _, root, suffix = split_domain(domain)
    if not root:
        return ""
    return f"{root}.{suffix}" if suffix else root


def min_distance_to_whitelist(root_domain: str, whitelist: set | None = None) -> float:
    """
    화이트리스트 중 가장 비슷한 도메인과의 '다른 비율' 반환 (0=완전 일치, 1=완전 다름)
    """
    if whitelist is None:
        whitelist = load_whitelist()

    if root_domain in whitelist:
        return 0.0

    best = process.extractOne(root_domain, whitelist, scorer=fuzz.ratio)
    if best is None:
        return 1.0

    _, score, _ = best
    return round(1 - score / 100, 4)
