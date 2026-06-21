## Context

The ingestion pipeline (`src/ingestion/pipeline.py`) currently treats every run as append-only: it skips a resume if its `resume_id` (PDF stem) appears in TinyDB, regardless of whether the underlying file has changed. ChromaDB stores chunks under IDs `{resume_id}_{i}` (0-indexed up to `chunk_count - 1`). TinyDB stores the structured record including `chunk_count` and `ingested_at`, but no content fingerprint.

There is no current mechanism to:
1. Detect that an existing PDF was replaced with different content.
2. Remove data for PDFs that have been deleted from disk.

Both gaps require a full wipe + re-ingest today.

## Goals / Non-Goals

**Goals:**
- Detect file content changes using a SHA-256 hash of the extracted text, stored in TinyDB
- On update: delete all existing ChromaDB chunks for the resume, remove its TinyDB record, then re-ingest fresh
- On deletion (file gone from disk): delete ChromaDB chunks and TinyDB record
- Emit new progress event kinds (`updated`, `deleted`) so callers can surface them
- Keep unchanged resumes truly untouched (no re-embedding, no LLM call)

**Non-Goals:**
- Tracking rename/move of PDFs across categories (treated as delete + add)
- Partial chunk updates (whole-document granularity only)
- Concurrency / locking across multiple simultaneous ingestion runs
- Rollback of a partially completed update

## Decisions

**Hash extracted text, not raw PDF bytes** — The text is already in memory when `extract_resumes()` yields it, so hashing it costs no extra I/O. Hashing raw bytes would also catch invisible metadata changes in the PDF that don't affect content, adding noise. Text hash is the right semantic boundary.

**SHA-256 hex digest** — Collision-resistant, fast on CPUs with SHA-NI, stdlib (`hashlib`). No new dependency needed.

**Delete-by-generated-IDs rather than ChromaDB `where` filter** — ChromaDB chunk IDs are deterministic (`{resume_id}_{i}` for `i in range(chunk_count)`). Using `collection.delete(ids=[...])` is O(chunk_count) and requires no metadata index scan. The `chunk_count` is available from the TinyDB record before deletion. Alternatively a `where={"resume_id": resume_id}` filter would work but is slower on large collections.

**Deletion sweep runs after the per-file loop** — All disk-resident files are processed first; then the pipeline takes the set difference between TinyDB resume IDs and the observed disk IDs to find orphans. This is a single pass and avoids any ordering dependency.

**New event shapes added, existing shapes unchanged** — The `"skipped"` event remains for hash-matching (truly unchanged) files. `"updated"` is emitted after a successful re-ingest of a changed file. `"deleted"` is emitted for each orphan removed. The final `"complete"` event gains `updated` and `deleted` counters (defaulting to 0), which is backwards-compatible since callers read by key.

## Risks / Trade-offs

- **Hash of extracted text vs source PDF**: If PyMuPDF's text extraction becomes non-deterministic across versions, the same PDF could produce a different hash and trigger spurious re-ingestion. → Acceptable: re-ingestion is correct, just unnecessary; text extraction has been stable in practice.
- **Partial update failure**: If ChromaDB deletion succeeds but re-ingestion errors out, the resume is removed from ChromaDB but still in TinyDB (or vice versa). → The pipeline error handler emits an `"error"` event; the operator can re-run ingestion which will re-detect the missing hash and retry. No data is permanently lost.
- **Large chunk counts**: Generating a list of IDs for `collection.delete()` for a 100-chunk resume is trivial. For pathological PDFs with thousands of chunks, the list is still small. Not a concern.

## Migration Plan

Existing TinyDB records have no `content_hash` field. On the first run after deployment:
- The pipeline reads each TinyDB record and finds no `content_hash` key.
- Treat missing hash as `None` → hash mismatch → full re-ingest of every previously indexed resume.
- This is a one-time cost equivalent to a full rebuild, but only on the first run. Subsequent runs are incremental.

No manual migration step is needed; the pipeline self-heals on first execution.
