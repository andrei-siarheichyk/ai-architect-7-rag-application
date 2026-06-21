## 1. Search Module

- [x] 1.1 Create `src/search/__init__.py` and `src/search/retriever.py` — embed query with `OllamaEmbedding(nomic-embed-text)`, query ChromaDB collection `resumes` for top-K chunks, return list of `{resume_id, category, text, distance}`
- [x] 1.2 Create `src/search/qa.py` — build prompt from retrieved chunks, call `gpt-4o-2024-11-20` via `AzureOpenAI` with `stream=True`, yield response chunks for Streamlit streaming

## 2. Streamlit Search Tab

- [x] 2.1 Refactor `app.py` to use `st.tabs(["Ingestion", "Search"])` — move existing ingestion UI into the Ingestion tab
- [x] 2.2 Add Search tab UI: query text input, top-K slider (1–10, default 5), Search button, results display (resume ID, category, matched text per result)
- [x] 2.3 Add Q&A section below results: question input, Ask button, `st.write_stream` for streamed answer, source resume IDs listed below answer
- [x] 2.4 Add guard: if ChromaDB collection is empty or missing, show warning "No resumes ingested yet — run ingestion first"
