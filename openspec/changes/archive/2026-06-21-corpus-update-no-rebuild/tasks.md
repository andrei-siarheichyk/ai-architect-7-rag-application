## 1. Chunker — deletion helper

- [x] 1.1 Add `delete_chunks(resume_id: str, chunk_count: int)` to `src/ingestion/chunker.py` that calls `collection.delete(ids=[f"{resume_id}_{i}" for i in range(chunk_count)])` on the ChromaDB collection

## 2. Structured extractor — store content hash

- [x] 2.1 Add `content_hash: str` parameter to `extract_structured()` in `src/ingestion/structured.py`
- [x] 2.2 Include `content_hash` in the TinyDB document dict passed to `db.upsert()`

## 3. Pipeline — hash-based diffing and deletion sweep

- [x] 3.1 Import `hashlib` at the top of `src/ingestion/pipeline.py`
- [x] 3.2 Add a helper `_text_hash(text: str) -> str` that returns `hashlib.sha256(text.encode()).hexdigest()`
- [x] 3.3 At the start of `run_ingestion()`, load all existing TinyDB records into a dict keyed by `resume_id` (for O(1) lookup)
- [x] 3.4 Track the set of `resume_id`s found on disk during the per-file loop
- [x] 3.5 For each resume, replace the current `if db.search(...)` skip check with hash comparison:
  - Compute `current_hash = _text_hash(text)`
  - If record exists and `record.get("content_hash") == current_hash` → yield `"skipped"` and continue
  - If record exists and hash differs → call `delete_chunks(resume_id, record["chunk_count"])`, remove TinyDB record, then fall through to ingest; yield `"updated"` instead of `"done"` after success
  - If no record → ingest as new, yield `"done"`
- [x] 3.6 Pass `content_hash=current_hash` to `extract_structured()` for all ingested (new or updated) resumes
- [x] 3.7 After the per-file loop, compute orphaned IDs: `set(existing_records.keys()) - seen_on_disk`; for each orphan call `delete_chunks()` and remove from TinyDB; yield a `"deleted"` event per orphan; accumulate a `deleted` counter
- [x] 3.8 Add `updated` and `deleted` integer counters to the final `"complete"` event

## 4. Streamlit UI — surface updated and deleted counts

- [x] 4.1 In `app.py` ingestion tab, update the success message to include `updated` and `deleted` from the `"complete"` event (e.g., `f"{event['updated']} updated, {event['deleted']} deleted"`)

## 5. Verify

- [x] 5.1 Run ingestion on the existing data folder; confirm all resumes are re-ingested (first run, no stored hashes) and complete event shows correct counts
- [x] 5.2 Run ingestion again immediately; confirm all resumes are skipped (hashes match)
- [x] 5.3 Manually alter one PDF or swap it with different content; confirm that resume is re-ingested and shows as `updated` in the UI
- [x] 5.4 Remove a PDF from the data folder; confirm it is deleted from ChromaDB and TinyDB and the `deleted` count increments
