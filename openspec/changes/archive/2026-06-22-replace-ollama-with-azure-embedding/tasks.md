## 1. Configuration

- [x] 1.1 In `src/config.py`, remove the `OLLAMA_BASE_URL` line and keep `EMBED_MODEL = "text-embedding-3-small-1"`
- [x] 1.2 Confirm `OPENAI_API_KEY`, `AZURE_ENDPOINT`, and `AZURE_API_VERSION` are present and point at `https://ai-proxy.lab.epam.com`

## 2. Ingestion embedding

- [x] 2.1 In `src/ingestion/chunker.py`, replace the `OllamaEmbedding` import with `from openai import AzureOpenAI` and import `EMBED_MODEL, OPENAI_API_KEY, AZURE_ENDPOINT, AZURE_API_VERSION` from `src.config`
- [x] 2.2 Replace the `_embed_model` singleton with an `AzureOpenAI` client singleton (`_get_client()`) mirroring the pattern in `src/ingestion/structured.py`
- [x] 2.3 In `chunk_and_store`, replace `get_text_embedding_batch(texts)` with a single `client.embeddings.create(model=EMBED_MODEL, input=texts)` call and map `resp.data[i].embedding` back in input order

## 3. Search embedding

- [x] 3.1 In `src/search/retriever.py`, replace the `OllamaEmbedding` import with `from openai import AzureOpenAI` and update the config import to the Azure variables
- [x] 3.2 Replace the `_embed_model` singleton with an `AzureOpenAI` client singleton (`_get_client()`)
- [x] 3.3 In `search`, replace `get_text_embedding(query)` with `client.embeddings.create(model=EMBED_MODEL, input=[query])` and read `resp.data[0].embedding`

## 4. Dependencies

- [x] 4.1 Remove `llama-index-embeddings-ollama` and `ollama` from `requirements.txt`
- [x] 4.2 Verify `openai` remains in `requirements.txt`

## 5. Documentation & migration

- [x] 5.1 Update `README.md` prerequisites: remove Ollama install / `ollama pull nomic-embed-text`; document the `text-embedding-3-small-1` model and DIAL API key
- [x] 5.2 Update the README Features/Ingestion description to say chunks are embedded via the EPAM DIAL / Azure OpenAI proxy
- [x] 5.3 Re-ingest resumes (delete `db/chroma` or re-run ingestion) so ChromaDB is rebuilt with 1536-dim vectors

## 6. Verification

- [x] 6.1 Run ingestion on at least one resume and confirm chunks are stored without errors
- [x] 6.2 Run a search query and confirm top-K results return; confirm a forced provider failure yields a clear error, not a crash
