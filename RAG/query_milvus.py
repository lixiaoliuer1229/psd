# /// script
# requires-python = ">=3.10"
# dependencies = ["pymilvus==2.6.17"]
# ///
"""List Milvus collections or read collection statistics through the SSH tunnel."""

import argparse
import json
import os

from pymilvus import MilvusClient, MilvusException


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--uri", default=os.getenv("MILVUS_URI", "http://127.0.0.1:19530"))
    parser.add_argument("--database", default=os.getenv("MILVUS_DATABASE", "chaintower"))
    parser.add_argument("--collection", help="Show the row count for this collection")
    args = parser.parse_args()

    try:
        client = MilvusClient(
            uri=args.uri,
            db_name=args.database,
            token=os.getenv("MILVUS_TOKEN", ""),
            timeout=10,
        )
        try:
            if args.collection:
                result = client.get_collection_stats(args.collection, timeout=10)
            else:
                result = client.list_collections(timeout=10)
        finally:
            client.close()
    except (MilvusException, ValueError) as error:
        parser.exit(1, f"Milvus query failed: {error}\n")

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
