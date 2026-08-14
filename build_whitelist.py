"""
Tranco Top 리스트에서 상위 N개 도메인을 뽑아 whitelist.txt 생성
"""

import pandas as pd
from pathlib import Path

INPUT_PATH = Path('data/top-1m.csv')   # rank, domain (헤더 없을 수 있음)
OUTPUT_PATH = Path('data/whitelist.txt')
TOP_N = 1000   # 상위 몇 개를 화이트리스트로 쓸지


def main():
    # Tranco CSV는 보통 헤더 없이 "rank,domain" 형식
    df = pd.read_csv(INPUT_PATH, header=None, names=['rank', 'domain'])
    print(f"[로드] {len(df):,}개 도메인")

    top_domains = df.head(TOP_N)['domain'].tolist()

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write('\n'.join(top_domains))

    print(f"[완료] {OUTPUT_PATH} 저장 (상위 {len(top_domains):,}개)")
    print("\n샘플 (앞 10개):")
    for d in top_domains[:10]:
        print(f"  {d}")


if __name__ == '__main__':
    main()