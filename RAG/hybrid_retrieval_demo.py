"""Retrieve through dense vectors, keywords and sample Doc2Query questions."""

import argparse
import math
import re
from operator import itemgetter

from pymilvus import MilvusClient

from bge_m3_demo import embed
from document_ingestion_demo import DOCUMENT_ID
from init_local_milvus import COLLECTION, DATABASE, LOCAL_URI, TIMEOUT
from permission_demo import document_filter

# Prepared questions stand in for the output of an offline Doc2Query job.
QUESTIONS = {
    f"{DOCUMENT_ID}:0": "休年假要提前几个工作日申请？",
    f"{DOCUMENT_ID}:1": "请病假几天以上需要医生证明？",
    f"{DOCUMENT_ID}:2": "出差回来怎么报销？",
}
DEFAULT_QUERY = "年假要提前几天申请？"


def retrieve(client: MilvusClient, query: str, scope: str) -> tuple[dict, dict]:
    rows = client.query(
        collection_name=COLLECTION, filter=scope,
        output_fields=["chunk_id", "text"], limit=20, timeout=TIMEOUT,
    )
    if not rows:
        raise RuntimeError("No visible chunks. Run document_ingestion_demo.py first.")
    chunks = {row["chunk_id"]: row["text"] for row in rows}
    questions = [(key, text) for key, text in QUESTIONS.items() if key in chunks]
    vector, *question_vectors = embed([query, *(text for _, text in questions)])
    dense = client.search(
        collection_name=COLLECTION, anns_field="embedding", data=[vector],
        filter=scope, limit=5, search_params={"metric_type": "COSINE"},
        output_fields=["chunk_id"], timeout=TIMEOUT,
    )[0]

    terms = set(re.findall(r"[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*", query.lower()))
    for phrase in ("年假", "病假", "差旅", "报销", "医疗证明"):
        if phrase in query:
            terms.add(phrase)
    keyword_scores = [(key, sum(term in text.lower() for term in terms))
                      for key, text in chunks.items()]
    question_scores = [
        (key, math.fsum(a * b for a, b in zip(vector, candidate, strict=True))
         / (math.hypot(*vector) * math.hypot(*candidate)))
        for (key, _), candidate in zip(questions, question_vectors, strict=True)
    ]
    return chunks, {
        "dense": [hit["entity"]["chunk_id"] for hit in dense],
        "keyword": [key for key, score in sorted(keyword_scores, key=itemgetter(1), reverse=True)
                    if score > 0],
        "doc2query": [key for key, _ in sorted(question_scores, key=itemgetter(1), reverse=True)],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="?", default=DEFAULT_QUERY)
    args = parser.parse_args()
    scope = document_filter("demo-tenant", "employee")
    client = MilvusClient(uri=LOCAL_URI, db_name=DATABASE, timeout=TIMEOUT)
    try:
        _, rankings = retrieve(client, args.query, scope)
        for branch, ids in rankings.items():
            print(f"{branch}: {ids}")
    finally:
        client.close()


if __name__ == "__main__":
    main()
