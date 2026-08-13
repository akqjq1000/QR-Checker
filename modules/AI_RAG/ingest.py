"""
KISA / MITRE / CISA 필터링된 JSONL 청크를 OpenAI 임베딩으로 벡터화하여
로컬 Chroma DB에 저장하는 스크립트.

결과:
    ./chroma_db/ 디렉토리에 영구 저장됨 (재실행해도 디스크에 남아있음,
    같은 id는 upsert되므로 중복 저장 걱정 없음)
"""

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
import chromadb
from tqdm import tqdm

load_dotenv()

EMBEDDING_MODEL = "text-embedding-3-small"  # 비용 대비 성능 좋음. 정확도 더 중요하면 -large로 교체
COLLECTION_NAME = "qr_quishing_kb"
current_dir = os.path.dirname(os.path.abspath(__file__))
CHROMA_DIR = os.path.join(current_dir, "docs", "chroma_db")
BATCH_SIZE = 100  # OpenAI 임베딩 API에 한 번에 보낼 텍스트 개수

# 이번 대화에서 만든 3개 필터링 결과 파일
INPUT_FILES = {
    "KISA": "kisa_filtered_chunks.jsonl",
    "MITRE": "mitre_filtered_chunks.jsonl",
    "CISA": "cisa_filtered_chunks.jsonl",
}

client = OpenAI()  # OPENAI_API_KEY 환경변수 자동 사용


def load_records(input_dir: Path) -> list[dict]:
    """3개 JSONL 파일을 모두 읽어 하나의 리스트로 합친다."""
    records = []
    for source, filename in INPUT_FILES.items():
        path = input_dir / filename
        if not path.exists():
            print(f"[경고] {path} 파일이 없어 건너뜁니다.")
            continue
        with path.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    records.append(json.loads(line))
    return records


def build_embedding_text(rec: dict) -> str:
    """임베딩할 텍스트 구성. title + body를 합쳐서 문맥을 살린다."""
    title = rec.get("title", "")
    body = rec.get("body", "")
    return f"{title}\n\n{body}".strip()


def flatten_metadata(rec: dict) -> dict:
    """Chroma 메타데이터는 str/int/float/bool만 허용 -> 리스트(matched_keywords)는
    쉼표로 join해서 문자열화. body는 documents 필드로 따로 저장하므로 메타데이터에서 제외."""
    meta = {}
    for k, v in rec.items():
        if k == "body":
            continue
        if isinstance(v, list):
            meta[k] = ", ".join(str(x) for x in v)
        elif v is None:
            meta[k] = ""
        else:
            meta[k] = v
    return meta


def embed_batch(texts: list[str]) -> list[list[float]]:
    resp = client.embeddings.create(model=EMBEDDING_MODEL, input=texts)
    # OpenAI가 반환 순서를 입력 순서와 동일하게 보장함
    return [d.embedding for d in resp.data]


def main():
    input_dir = Path(__file__).parent / "docs"
    # input_dir = Path(__file__).parent  # jsonl 파일들을 이 스크립트와 같은 폴더에 둔다고 가정
    records = load_records(input_dir)
    print(f"총 {len(records)}개 청크 로드됨")

    if not records:
        print("로드된 레코드가 없습니다. jsonl 파일 경로를 확인하세요.")
        return

    chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = chroma_client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    for i in tqdm(range(0, len(records), BATCH_SIZE), desc="임베딩 + 저장 중"):
        batch = records[i: i + BATCH_SIZE]
        texts = [build_embedding_text(r) for r in batch]

        embeddings = embed_batch(texts)

        collection.upsert(
            ids=[r["id"] for r in batch],
            embeddings=embeddings,
            documents=[r.get("body", "") for r in batch],
            metadatas=[flatten_metadata(r) for r in batch],
        )

    print(f"완료. 컬렉션 '{COLLECTION_NAME}'에 {collection.count()}개 항목 저장됨")
    print(f"저장 위치: {Path(CHROMA_DIR).resolve()}")


if __name__ == "__main__":
    main()
