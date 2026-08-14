from pathlib import Path
from functools import lru_cache
from rapidfuzz import process, fuzz

from .url_to_feature import split_domain  # root domain 계산의 단일 소스 (재사용)

BASE_DIR = Path(__file__).resolve().parent.parent
WHITELIST_PATH = BASE_DIR / "data" / "whitelist.txt"


@lru_cache(maxsize=1)
def load_whitelist() -> set:
    with open(WHITELIST_PATH, encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())


# 스킴이 있는 URL이 오면 안 됨
def extract_root_domain(url_or_domain: str) -> str:
    """url_to_feature.split_domain을 재사용해 root domain(root+suffix)을 구한다.

    자체적으로 tldextract를 다시 호출하지 않고, 프로젝트 전체에서
    root domain을 계산하는 유일한 소스인 split_domain의 결과를 그대로 씀.
    """
    domain = url_or_domain.split("/", 1)[0].split(":", 1)[0]
    _, root, suffix = split_domain(domain)
    if not root:
        return ""
    return f"{root}.{suffix}" if suffix else root


def min_distance_to_whitelist(root_domain: str, whitelist: set = None) -> float:
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