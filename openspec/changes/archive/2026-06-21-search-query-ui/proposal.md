## Why

The ingestion pipeline stores 2400+ resumes in ChromaDB and TinyDB, but there is no way to query or search them. Users need a Streamlit UI tab to ask natural language questions and retrieve relevant resumes from the vector store.

## What Changes

- Add a **Search** tab to the existing Streamlit app (`app.py`)
- Implement semantic search against ChromaDB using `nomic-embed-text` embeddings
- Display retrieved resume chunks with metadata (resume ID, category, relevance)
- Add a natural language Q&A mode: user asks a question, retrieved chunks are sent to `gpt-4o-2024-11-20` via EPAM DIAL, answer is displayed alongside sources

## Capabilities

### New Capabilities
- `resume-search`: Semantic search over ingested resume chunks — embed query with nomic-embed-text, retrieve top-K chunks from ChromaDB, display results with resume ID, category, and matched text
- `resume-qa`: Natural language Q&A — retrieved chunks used as context for an LLM-generated answer via EPAM DIAL (AzureOpenAI)

### Modified Capabilities
- *(none)*

## Impact

- `app.py` — add Search tab alongside existing Ingestion tab
- New `src/search/` module — query and QA logic
- Depends on: ChromaDB collection `resumes`, `nomic-embed-text` via Ollama, `gpt-4o-2024-11-20` via EPAM DIAL
