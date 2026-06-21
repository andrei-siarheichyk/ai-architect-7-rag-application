## Context

The ingestion pipeline (change: `initial`) populates:
- **ChromaDB** collection `resumes` — text chunks with `nomic-embed-text` embeddings, metadata: `resume_id`, `category`, `chunk_index`, `total_chunks`
- **TinyDB** — structured resume documents keyed by `resume_id`

The Streamlit app currently has one tab (Ingestion). This change adds a Search tab.

## Goals / Non-Goals

**Goals:**
- Semantic search: embed a user query with `nomic-embed-text`, retrieve top-K matching chunks from ChromaDB
- Display results: resume ID, category, matched text snippet
- Q&A mode: send retrieved chunks as context to `gpt-4o-2024-11-20` (EPAM DIAL), stream the answer back

**Non-Goals:**
- Filtering by category, skills, or date (visualization phase)
- Pagination of results
- Saving or exporting search results

## Decisions

**Query embedding: reuse `OllamaEmbedding` from chunker**
Same model (`nomic-embed-text`) used at ingestion — ensures embedding space consistency. Alternative (OpenAI embeddings) would break similarity because vectors would be in a different space.

**Separate `src/search/` module**
Keeps retrieval logic out of `app.py`. `retriever.py` handles ChromaDB queries; `qa.py` handles LLM calls. Alternative (inline in app.py) makes the UI file hard to test.

**Streaming LLM answer**
EPAM DIAL supports streaming via `stream=True`. Streamlit's `st.write_stream` renders tokens as they arrive — better UX for long answers. Alternative (wait for full response) feels slow.

**Top-K default: 5**
Balances context window usage vs. coverage. Configurable via a slider in the UI.

## Risks / Trade-offs

- **ChromaDB empty** → search returns nothing. UI must detect `col.count() == 0` and prompt user to run ingestion first.
- **Ollama not running** → embedding query fails. Wrap in try/except, show clear error message.
- **LLM hallucination** → answer may not be grounded in retrieved chunks. Display source chunks alongside answer so user can verify.

## Module layout

```
src/
└── search/
    ├── __init__.py
    ├── retriever.py   # embed query → ChromaDB search → return results
    └── qa.py          # results → AzureOpenAI prompt → streamed answer
```

## Streamlit UI shape

```
[ Ingestion ] [ Search ]   ← tabs

Search tab:
  Query: [________________________] [Search]
  Top-K: [slider 1–10, default 5]

  Results (semantic search):
  ┌──────────────────────────────────────────┐
  │ #1  Resume: 16852740  Category: Finance  │
  │ "...managed portfolio of $50M across..." │
  └──────────────────────────────────────────┘

  Ask a question about results:
  [________________________] [Ask]
  ▸ Answer streamed here...

  Sources used: 16852740, 29384756, ...
```
