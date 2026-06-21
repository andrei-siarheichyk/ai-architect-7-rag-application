# Tasks — Ingestion Pipeline

- [x] T1: Project scaffolding — create folder structure, `requirements.txt`, and `src/config.py` with paths and model settings
- [x] T2: PDF extractor — `src/ingestion/extractor.py`: walk `data/<Category>/<ID>.pdf`, extract text with PyMuPDF, yield `(resume_id, category, text)`
- [x] T3: ChromaDB chunker — `src/ingestion/chunker.py`: split text with LlamaIndex SentenceSplitter, embed with nomic-embed-text via Ollama, store chunks in ChromaDB
- [x] T4: Structured extractor — `src/ingestion/structured.py`: call Qwen3 via Ollama to extract skills/years_exp/education/job_titles/certifications as JSON, store in TinyDB
- [x] T5: Ingestion orchestrator — `src/ingestion/pipeline.py`: wire extractor → chunker → structured, skip already-ingested resumes, yield progress events
- [x] T6: Streamlit UI — `app.py`: folder path input, Start button, progress bar, live status, completion summary table
