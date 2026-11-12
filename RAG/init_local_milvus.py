# /// script
# requires-python = ">=3.10"
# dependencies = ["pymilvus==2.6.17"]
# ///
"""Initialize the local RAG demo database and collection."""

from pymilvus import DataType, MilvusClient

LOCAL_URI = "http://127.0.0.1:19531"
DATABASE = "rag_local"
COLLECTION = "document_chunks"
EMBEDDING_DIM = 1024
TIMEOUT = 10


def main() -> None:
    client = MilvusClient(uri=LOCAL_URI, timeout=TIMEOUT)
    try:
        version = client.get_server_version(timeout=TIMEOUT)
        if not version.startswith("milvus_lite-"):
            raise SystemExit(f"Expected local Milvus Lite at {LOCAL_URI}, got {version}")

        if DATABASE not in client.list_databases(timeout=TIMEOUT):
            client.create_database(DATABASE, timeout=TIMEOUT)
        client.use_database(DATABASE, timeout=TIMEOUT)

        if client.has_collection(COLLECTION, timeout=TIMEOUT):
            print(f"{DATABASE}.{COLLECTION} already exists")
            return

        schema = MilvusClient.create_schema(auto_id=False, enable_dynamic_field=False)
        schema.add_field("chunk_id", DataType.VARCHAR, is_primary=True, max_length=128)
        schema.add_field("document_id", DataType.VARCHAR, max_length=128)
        schema.add_field("chunk_index", DataType.INT64)
        schema.add_field("text", DataType.VARCHAR, max_length=65535)
        schema.add_field("embedding", DataType.FLOAT_VECTOR, dim=EMBEDDING_DIM)

        indexes = client.prepare_index_params()
        indexes.add_index(field_name="embedding", index_type="FLAT", metric_type="COSINE")
        client.create_collection(
            collection_name=COLLECTION,
            schema=schema,
            index_params=indexes,
            timeout=TIMEOUT,
        )
        print(f"Created {DATABASE}.{COLLECTION}")
    finally:
        client.close()


if __name__ == "__main__":
    main()
