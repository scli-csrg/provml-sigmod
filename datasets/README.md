# ProvML Evaluation Datasets

Two workflows, four violation classes each, plus benign runs.

- W1: compile-load-deploy
- W2: RAG ingest-retrieve-generate

Each has `benign_runs.jsonl` (50) plus `injected_{missing,mismatched,replayed,forged}.jsonl` (100 each).

No real model weights are distributed; all artifacts are synthetic, content-addressed byte streams.
