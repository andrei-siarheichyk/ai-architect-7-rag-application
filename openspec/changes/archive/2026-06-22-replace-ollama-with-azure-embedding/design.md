## Context

The Python RAG app produces embeddings in two places — `src/ingestion/chunker.py` (batch-embed resume chunks before storing in ChromaDB) and `src/search/retriever.py` (embed a single query at search time). Both instantiate `OllamaEmbedding` from `llama-index-embeddings-ollama`, pointed at `OLLAMA_BASE_URL` with model `EMBED_MODEL`.

Meanwhile `src/ingestion/structured.py` and `src/search/qa.py` already talk to the EPAM DIAL proxy (`https://ai-proxy.lab.epam.com`) through the `openai` package's `AzureOpenAI` client, using `OPENAI_API_KEY`, `AZURE_ENDPOINT`, and `AZURE_API_VERSION` from config. The DIAL proxy exposes an Azure OpenAI-compatible embeddings endpoint, so embeddings can use the same client and credentials. The working tree already points `OLLAMA_BASE_URL`/`EMBED_MODEL` at the proxy and the `text-embedding-3-small-1` model name, but the code still uses the Ollama client, which is the mismatch this change resolves.

## Goals / Non-Goals

**Goals:**
- Generate both ingestion and query embeddings through the DIAL / Azure OpenAI-compatible endpoint using `text-embedding-3-small-1`.
- Reuse the existing `AzureOpenAI` client pattern and the existing credential config — no new auth surface.
- Keep the `chunk_and_store` / `search` public interfaces unchanged so callers (app.py, ingestion pipeline) need no edits.
- Remove the Ollama runtime dependency.

**Non-Goals:**
- No changes to the .NET implementation (`ResumeRag/`, `dotnet-*` specs).
- No automatic migration of the existing ChromaDB collection; re-ingestion is expected.
- No change to chunking strategy, ChromaDB schema, or retrieval/ranking logic.
- No abstraction layer or provider-switching toggle — single provider.

## Decisions

**Decision: Use the `openai` `AzureOpenAI` client for embeddings, mirroring `structured.py`/`qa.py`.**
The codebase already depends on `openai` and has a proven lazy-singleton client pattern for the DIAL proxy. Each module keeps a module-level `_client: AzureOpenAI | None` initialized via `_get_client()` with `api_key=OPENAI_API_KEY`, `azure_endpoint=AZURE_ENDPOINT`, `api_version=AZURE_API_VERSION`. Embeddings are produced with `client.embeddings.create(model=EMBED_MODEL, input=...)` and read from `resp.data[i].embedding`.
- *Alternative considered:* `llama-index-embeddings-azure-openai`. Rejected — it adds another dependency and a second config style for the same proxy already reached via the plain `openai` client.
- *Alternative considered:* keep `OllamaEmbedding` pointed at the proxy. Rejected — the Ollama embeddings API shape differs from the OpenAI/Azure embeddings API the DIAL proxy serves, so it is not a reliable transport here.

**Decision: Preserve config variable names where practical, but rename `OLLAMA_BASE_URL`.**
`EMBED_MODEL` stays. `OLLAMA_BASE_URL` is misleading once Ollama is gone; the embedding client reads `AZURE_ENDPOINT` (already in config and equal to the same proxy URL), so the separate `OLLAMA_BASE_URL` line is removed.

**Decision: Batch ingestion embeddings in one `embeddings.create` call.**
`chunk_and_store` already collects all chunk `texts` and calls `get_text_embedding_batch`. The Azure/OpenAI embeddings endpoint accepts a list `input`, so pass the full `texts` list and map `resp.data` back in order. Query embedding passes a single-element list and reads `data[0]`.

## Risks / Trade-offs

- **Embedding dimensions change (768 → 1536), making the existing ChromaDB collection incompatible** → Document re-ingestion in the migration plan and README; ChromaDB raises a dimension-mismatch error on query against an old collection, which surfaces clearly rather than silently corrupting results.
- **Network/auth dependency for every embedding call (no local fallback)** → The whole app already depends on the DIAL proxy for chat; failures surface through the existing per-call error handling, and the search spec keeps an "embedding provider unavailable" scenario.
- **Per-call latency and proxy rate limits on large ingestions** → Batch all chunks of a resume in a single request; ingestion is already an explicit, non-interactive step.
- **`embeddings.create` preserves input order in `data`** → Rely on the documented OpenAI contract (results returned in input order); map by index, do not assume any reordering.

## Migration Plan

1. Update `requirements.txt` (remove `llama-index-embeddings-ollama`, `ollama`).
2. Swap the embedding client in `chunker.py` and `retriever.py`; update `config.py`.
3. Re-ingest resumes so ChromaDB is rebuilt with 1536-dim vectors (delete `db/chroma` or re-run ingestion over the data set).
4. Rollback: revert the commit and re-install the Ollama embedding dependency; the old 768-dim collection is then valid again.
