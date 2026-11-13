"""Merge retrieval rankings with weighted RRF, then call BGE Reranker."""

import json
import os
from collections import defaultdict
from urllib.error import URLError
from urllib.request import Request, urlopen

from pymilvus import MilvusClient

from hybrid_retrieval_demo import DEFAULT_QUERY, retrieve
from init_local_milvus import DATABASE, LOCAL_URI, TIMEOUT
from permission_demo import document_filter

WEIGHTS = {"dense": 1.0, "keyword": 0.8, "doc2query": 1.0}


def fuse(rankings: dict, k: int = 60) -> list[str]:
    scores = defaultdict(float)
    for branch, ids in rankings.items():
        seen = set()
        for rank, chunk_id in enumerate(ids, start=1):
            if chunk_id not in seen:
                scores[chunk_id] += WEIGHTS[branch] / (k + rank)
                seen.add(chunk_id)
    return sorted(scores, key=lambda chunk_id: (-scores[chunk_id], chunk_id))


def rerank(query: str, ids: list[str], chunks: dict, top_k: int = 3) -> list[str]:
    if not ids:
        return []
    endpoint = os.getenv("BGE_RERANK_URL", "http://127.0.0.1:18002/v1/rerank")
    request = Request(
        endpoint,
        data=json.dumps({"query": query, "documents": [chunks[key] for key in ids],
                         "top_n": min(top_k, len(ids))}).encode(),
        headers={"Content-Type": "application/json"}, method="POST",
    )
    try:
        with urlopen(request, timeout=15) as response:
            indexes = [row["index"] for row in json.load(response)["results"]]
        if (len(indexes) != min(top_k, len(ids)) or len(set(indexes)) != len(indexes)
                or any(type(index) is not int or not 0 <= index < len(ids) for index in indexes)):
            raise ValueError("Invalid rerank indexes")
        return [ids[index] for index in indexes]
    except (URLError, TimeoutError, ValueError, KeyError, TypeError) as error:
        print(f"Reranker unavailable ({error}); using RRF order")
        return ids[:top_k]


def main() -> None:
    client = MilvusClient(uri=LOCAL_URI, db_name=DATABASE, timeout=TIMEOUT)
    try:
        chunks, rankings = retrieve(client, DEFAULT_QUERY, document_filter("demo-tenant", "employee"))
        fused = fuse(rankings)
        print(f"RRF: {fused}")
        print(f"Rerank: {rerank(DEFAULT_QUERY, fused, chunks)}")
    finally:
        client.close()


if __name__ == "__main__":
    main()
