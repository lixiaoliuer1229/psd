"""Compare dense retrieval and RRF using the same labeled queries."""

import math
from statistics import mean

from pymilvus import MilvusClient

from document_ingestion_demo import DOCUMENT_ID
from fusion_rerank_demo import fuse
from hybrid_retrieval_demo import retrieve
from init_local_milvus import DATABASE, LOCAL_URI, TIMEOUT
from permission_demo import document_filter

CASES = (
    ("休年假需要提前多久报备？", f"{DOCUMENT_ID}:0"),
    ("请病假什么时候要交证明？", f"{DOCUMENT_ID}:1"),
    ("EXP-01 是什么流程？", f"{DOCUMENT_ID}:2"),
)


def metrics(ranks: list[int], k: int) -> dict:
    hits = [rank if 0 < rank <= k else 0 for rank in ranks]
    # Each case has one relevant chunk, so its ideal discounted gain is 1.
    return {
        f"Recall@{k}": mean(rank > 0 for rank in hits),
        f"MRR@{k}": mean(1 / rank if rank else 0 for rank in hits),
        f"NDCG@{k}": mean(1 / math.log2(rank + 1) if rank else 0 for rank in hits),
    }


def main() -> None:
    scope = document_filter("demo-tenant", "employee")
    ranks = {"dense": [], "rrf": []}
    client = MilvusClient(uri=LOCAL_URI, db_name=DATABASE, timeout=TIMEOUT)
    try:
        for query, expected in CASES:
            _, rankings = retrieve(client, query, scope)
            for mode, ids in (("dense", rankings["dense"]), ("rrf", fuse(rankings))):
                ranks[mode].append(ids.index(expected) + 1 if expected in ids else 0)
    finally:
        client.close()
    for mode, positions in ranks.items():
        print(mode, "ranks:", positions, metrics(positions, k=2))


if __name__ == "__main__":
    main()
