## Why

The Python app embeds resume chunks and search queries through a locally-hosted Ollama (`nomic-embed-text`), which requires every developer to install and run Ollama separately and pull a model. The rest of the app already authenticates to the EPAM DIAL proxy (`https://ai-proxy.lab.epam.com`) for chat completions via the Azure OpenAI-compatible client. Routing embeddings through the same proxy removes the local Ollama dependency, unifies on one provider/credential, and uses the higher-quality `text-embedding-3-small-1` model.

## What Changes

- Replace the `OllamaEmbedding` client used for ingestion and search with the EPAM DIAL / Azure OpenAI-compatible embedding endpoint, using model `text-embedding-3-small-1`.
- Embeddings authenticate with the same `OPENAI_API_KEY` / `AZURE_ENDPOINT` / `AZURE_API_VERSION` config already used for chat completions.
- Remove the local Ollama prerequisite (install + `ollama pull`) from setup; embeddings now require only the DIAL API key.
- Drop the `llama-index-embeddings-ollama` and `ollama` dependencies; add no new runtime dependency (the `openai` client is already present).
- **BREAKING**: The embedding model changes from `nomic-embed-text` (768 dims) to `text-embedding-3-small-1` (1536 dims). The existing ChromaDB collection is incompatible and must be re-ingested.

## Capabilities

### New Capabilities
- `text-embedding`: Generating embedding vectors for text via the EPAM DIAL / Azure OpenAI-compatible proxy, shared by ingestion and search.

### Modified Capabilities
- `resume-search`: Query embedding now uses `text-embedding-3-small-1` via the DIAL proxy instead of `nomic-embed-text` via Ollama; the failure scenario covers the embedding provider rather than Ollama specifically.
- `project-readme`: Prerequisites and the ingestion overview drop the Ollama install / `ollama pull` step in favor of the DIAL embedding model and API key.

## Impact

- Code: `src/config.py`, `src/ingestion/chunker.py`, `src/search/retriever.py`.
- Dependencies: remove `llama-index-embeddings-ollama` and `ollama` from `requirements.txt`.
- Data: existing `db/chroma` collection must be re-ingested due to the dimension change.
- Docs: `README.md` setup/prerequisites.
- Out of scope: the parallel .NET implementation (`ResumeRag/`, `dotnet-*` specs) is unchanged.
