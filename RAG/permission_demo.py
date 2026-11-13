"""Scope Milvus retrieval using a trusted demo identity and document ACL."""

import json

from pymilvus import MilvusClient

from document_ingestion_demo import DOCUMENT_ID
from init_local_milvus import COLLECTION, DATABASE, LOCAL_URI, TIMEOUT

# In an application these values come from authentication and the server-side ACL.
ACCESS = {("demo-tenant", "employee"): (DOCUMENT_ID,)}


def document_filter(tenant: str, user: str) -> str:
    allowed = ACCESS.get((tenant, user), ())
    if not allowed:
        raise PermissionError("No readable documents")
    return f"document_id in {json.dumps(allowed, ensure_ascii=False)}"


def main() -> None:
    client = MilvusClient(uri=LOCAL_URI, db_name=DATABASE, timeout=TIMEOUT)
    try:
        for user in ("employee", "guest"):
            try:
                scope = document_filter("demo-tenant", user)
            except PermissionError:
                print(f"{user}: access denied before querying Milvus")
                continue
            rows = client.query(
                collection_name=COLLECTION,
                filter=scope,
                output_fields=["chunk_id"],
                limit=20,
                timeout=TIMEOUT,
            )
            print(f"{user}: {[row['chunk_id'] for row in rows]}")
    finally:
        client.close()


if __name__ == "__main__":
    main()
