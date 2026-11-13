# RAG 分步 demo

在此目录使用已配置的 Python 3.12 `.venv`（PyCharm 也可以直接运行各脚本）。依赖为 `pymilvus==2.6.17`，可用 `uv pip install --python .venv/bin/python pymilvus==2.6.17` 安装。

Milvus Lite 使用本机 `127.0.0.1:19531` 的 `rag_local.document_chunks`。BGE-M3 和 BGE Reranker 默认通过 SSH 隧道访问本机端口 `18001` 和 `18002`，可以分别用 `BGE_M3_EMBEDDING_URL` 和 `BGE_RERANK_URL` 覆盖。

```bash
.venv/bin/python init_local_milvus.py
.venv/bin/python document_ingestion_demo.py
.venv/bin/python permission_demo.py
.venv/bin/python hybrid_retrieval_demo.py "EXP-01 是什么流程？"
.venv/bin/python fusion_rerank_demo.py
.venv/bin/python cited_answer_demo.py
.venv/bin/python retrieval_evaluation_demo.py
```

1. 入库读取示例 Markdown，按空行切分正文，并按稳定片段 ID 更新向量和原文。
2. 权限用固定的教学身份和 ACL 展示查询前过滤。真实服务应从鉴权和权限存储获取这些数据。
3. 混合召回包含 Milvus 向量检索、简化关键词匹配，以及预先编写的 Doc2Query 问题。示例为方便观察，在查询时编码这些问题。生产实现应在入库时编码并建立独立索引。
4. 加权 RRF 用各路名次合并结果，再请求 BGE Reranker。重排请求失败时输出提示并采用 RRF 顺序。
5. 引用回答默认直接摘录第一条证据。要调用真实大模型，请设置 `RAG_CHAT_COMPLETIONS_URL`（完整的 OpenAI 兼容 Chat Completions 地址）、`RAG_CHAT_MODEL`，以及需要时的 `RAG_CHAT_API_KEY`。引用编号校验只检查是否指向提供的来源。
6. 评测用三条人工标注问题比较纯向量和 RRF，打印 Recall@2、MRR@2、NDCG@2。这些小样本用于演示指标计算。

脚本用的是合成示例数据，适合发送给现有模型服务。线上 Milvus 的只读查询仍由 `query_milvus.py` 提供。
