"""Read, split, embed and upsert a sample Markdown document."""

import re
from pathlib import Path

from pymilvus import MilvusClient

from bge_m3_demo import embed
from init_local_milvus import COLLECTION, DATABASE, LOCAL_URI, TIMEOUT

DOCUMENT_ID = "demo-employee-handbook"
SAMPLE = Path(__file__).with_name("demo_document.md")


def split_document(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    return [
        block.strip()
        for block in re.split(r"\n\s*\n", text)
        if block.strip() and not block.lstrip().startswith("#")
    ]


def main() -> None:
    chunks = split_document(SAMPLE)
    if not chunks or any(len(chunk.encode("utf-8")) > 65535 for chunk in chunks):
        raise SystemExit("Expected nonempty chunks of at most 65535 UTF-8 bytes")
    client = MilvusClient(uri=LOCAL_URI, db_name=DATABASE, timeout=TIMEOUT)
    try:
        if not client.get_server_version(timeout=TIMEOUT).startswith("milvus_lite-"):
            raise SystemExit("This demo writes only to the local Milvus Lite instance")
        rows = [
            {
                "chunk_id": f"{DOCUMENT_ID}:{index}",
                "document_id": DOCUMENT_ID,
                "chunk_index": index,
                "text": chunk,
                "embedding": vector,
            }
            for index, (chunk, vector) in enumerate(zip(chunks, embed(chunks), strict=True))
        ]
        result = client.upsert(collection_name=COLLECTION, data=rows, timeout=TIMEOUT)
        print(f"Upserted {result['upsert_count']} chunks into {DATABASE}.{COLLECTION}")
    finally:
        client.close()


if __name__ == "__main__":
    main()
