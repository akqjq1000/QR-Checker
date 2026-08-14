from .domain_similarity import extract_root_domain, min_distance_to_whitelist, load_whitelist

def test():
    wl = load_whitelist()

    cases = [
        ("google.com", 0.0),
        ("goog1e.com", None),
        ("m.wikipedia.org", 0.0),
        ("en.wikipedia.org", 0.0),
    ]

    for url, expected in cases:
        root = extract_root_domain(url)
        dist = min_distance_to_whitelist(root, wl)
        print(f"{url:25s} -> root={root:20s} dist={dist}")
        if expected is not None:
            assert abs(dist - expected) < 1e-6, f"FAIL: {url} expected {expected}, got {dist}"

    print("PASS (goog1e.com 결과는 위 출력에서 눈으로 확인)")

if __name__ == "__main__":
    test()