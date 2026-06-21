## Why

The current ingestion pipeline only checks whether a `resume_id` already exists in TinyDB; it has no way to detect that a PDF has changed, and it never removes stale entries when a PDF is deleted from disk. The only recovery path today is wiping both databases and re-running a full ingestion, which is expensive and destroys all indexed data. Adding content-hash diffing and deletion detection enables incremental corpus maintenance with surgical ChromaDB updates.

## What Changes

- Store a SHA-256 hash of the extracted text alongside each TinyDB record at ingestion time
- On re-ingestion, compute the hash of each found PDF and compare against the stored hash:
  - **Unchanged** (hash matches) → skip, same as before
  - **Updated** (hash differs) → delete the resume's existing chunks from ChromaDB and its TinyDB record, then re-ingest
  - **New** (no TinyDB record) → ingest as before
- After processing all found PDFs, identify resume IDs present in TinyDB but absent from disk and delete them from both ChromaDB and TinyDB
- Add two new progress event statuses: `"updated"` (re-ingested after change) and `"deleted"` (removed from both stores)
- Surface updated and deleted counts in the final `"complete"` event and in the Streamlit ingestion UI

## Capabilities

### New Capabilities

- `incremental-ingestion`: Per-document content-hash diffing and stale-entry deletion during ingestion; enables corpus updates without a full vector DB rebuild

### Modified Capabilities

(none — no existing spec-level contracts change)

## Impact

- `src/ingestion/pipeline.py`: Core change — hash comparison logic, delete-on-update, delete-on-removal sweep
- `src/ingestion/structured.py`: `extract_structured()` gains a `content_hash` parameter, stores it in the TinyDB document
- `src/ingestion/extractor.py`: `extract_resumes()` must also yield the file path so the pipeline can compute the hash from raw bytes (avoids re-reading the file); alternatively hash the already-extracted text (simpler, chosen approach)
- `src/ingestion/chunker.py`: New `delete_chunks(resume_id, chunk_count)` helper to remove chunks from ChromaDB by generated IDs
- `app.py`: Ingestion tab updated to display updated/deleted counts in the completion summary
- No new dependencies (hashlib is stdlib)
