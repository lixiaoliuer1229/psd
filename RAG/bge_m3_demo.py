# /// script
# requires-python = ">=3.10"
# dependencies = ["pymilvus==2.6.17"]
# ///
"""Embed sample chunks with BGE-M3 and retrieve them from local Milvus Lite."""

import json
import math
import os
from urllib.request import Request, urlopen

from pymilvus import MilvusClient

from init_local_milvus import COLLECTION, DATABASE, EMBEDDING_DIM, LOCAL_URI, TIMEOUT

MODEL = "BGE-M3"
DOCUMENT_ID = "demo-leave-policy"
SAMPLES = (
    "申请年假需至少提前三个工作日提交申请，由直属主管审批。",
    "员工因病请假，应尽快通知主管。连续病假超过两天需提供医疗证明。",
    "报销差旅费用时，请保留交通和住宿发票，并在返程后提交报销单。",
)


def embed(texts: list[str]) -> list[list[float]]:
    endpoint = os.getenv("BGE_M3_EMBEDDING_URL", "http://127.0.0.1:18001/v1/embeddings")
    request = Request(
        endpoint,
        data=json.dumps({"model": MODEL, "input": texts}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=60) as response:
        items = sorted(json.load(response)["data"], key=lambda item: item["index"])
    if [item["index"] for item in items] != list(range(len(texts))):
        raise ValueError("BGE-M3 returned unexpected embedding indexes")
    vectors = [item["embedding"] for item in items]
    if any(len(vector) != EMBEDDING_DIM or not all(map(math.isfinite, vector)) for vector in vectors):
        raise ValueError(f"Expected finite {EMBEDDING_DIM}-dimensional dense vectors")
    return vectors


def main() -> None:
    question = "年假要提前几天申请？"
    client = MilvusClient(uri=LOCAL_URI, db_name=DATABASE, timeout=TIMEOUT)
    try:
        if not client.get_server_version(timeout=TIMEOUT).startswith("milvus_lite-"):
            raise SystemExit(f"Expected local Milvus Lite at {LOCAL_URI}")

        *vectors, query_vector = embed([*SAMPLES, question])
        rows = [
            {
                "chunk_id": f"{DOCUMENT_ID}:{index}",
                "document_id": DOCUMENT_ID,
                "chunk_index": index,
                "text": chunk,
                "embedding": vector,
            }
            for index, (chunk, vector) in enumerate(zip(SAMPLES, vectors, strict=True))
        ]
        result = client.upsert(collection_name=COLLECTION, data=rows, timeout=TIMEOUT)
        print(f"Upserted {result['upsert_count']} chunks into {DATABASE}.{COLLECTION}")

        hits = client.search(
            collection_name=COLLECTION,
            anns_field="embedding",
            data=[query_vector],
            filter='document_id == "demo-leave-policy"',
            limit=3,
            search_params={"metric_type": "COSINE"},
            output_fields=["chunk_id", "text"],
            timeout=TIMEOUT,
        )
        print(question)
        print(json.dumps(hits[0], ensure_ascii=False, indent=2))
    finally:
        client.close()


if __name__ == "__main__":
    main()
