# Ingestion Pipeline — Resume Dataset

## What
Build the ingestion pipeline that processes PDF resumes from the Kaggle resume dataset into two stores:
- **ChromaDB** — text chunks with embeddings for semantic search
- **TinyDB** — structured fields (skills, experience, education) for analytics

## Why
This is the foundation layer of the resume analyzer app. Without ingested data, no queries or visualizations are possible.

## In scope
- Walk `/data/<Category>/<resume_id>.pdf` folder structure
- Extract text from PDFs using PyMuPDF
- Chunk text and embed with `nomic-embed-text` via Ollama → store in ChromaDB
- Extract structured fields with `qwen3` via Ollama → store in TinyDB
- Skip already-ingested resumes (idempotent re-runs)
- Streamlit UI: trigger ingestion, show progress, show completion summary

## Non-goals
- Search / query interface (next phase)
- Visualization / charts (future phase)
- CSV-based ingestion (PDF-first)
- Cloud deployment

## Stack
| Layer | Choice |
|-------|--------|
| LLM | qwen3 via Ollama (localhost:11434) |
| Embeddings | nomic-embed-text via Ollama |
| PDF parsing | PyMuPDF |
| RAG framework | LlamaIndex |
| Vector store | ChromaDB (persistent, embedded) |
| Document store | TinyDB |
| UI | Streamlit |
