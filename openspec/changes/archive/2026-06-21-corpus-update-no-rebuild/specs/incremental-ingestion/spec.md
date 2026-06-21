## ADDED Requirements

### Requirement: Content hash stored per resume
The system SHALL compute a SHA-256 hex digest of the extracted text for each resume and persist it in the TinyDB record under the key `content_hash` at ingestion time.

#### Scenario: Hash written on first ingest
- **WHEN** a resume is ingested for the first time
- **THEN** the TinyDB record SHALL contain a `content_hash` field with the SHA-256 hex digest of the extracted text

### Requirement: Unchanged resumes are skipped
During ingestion the pipeline SHALL compare the computed hash of each found PDF against the stored `content_hash` in TinyDB. If the hashes match the resume SHALL be skipped without touching ChromaDB or calling the LLM.

#### Scenario: Unchanged file skipped
- **WHEN** a PDF exists on disk and its text hash matches the stored `content_hash`
- **THEN** the pipeline SHALL emit a `"skipped"` event and SHALL NOT re-embed or re-call the LLM for that resume

### Requirement: Changed resume triggers in-place update
If a PDF's computed hash differs from the stored `content_hash` (including when `content_hash` is absent), the pipeline SHALL delete all existing ChromaDB chunks for that resume and its TinyDB record, then re-ingest the resume from scratch.

#### Scenario: Updated file re-ingested
- **WHEN** a PDF exists on disk and its text hash differs from the stored `content_hash`
- **THEN** the pipeline SHALL delete chunks with IDs `{resume_id}_0` through `{resume_id}_{chunk_count - 1}` from ChromaDB, remove the TinyDB record, re-chunk and re-embed the new text, and emit an `"updated"` event

#### Scenario: Missing hash treated as changed
- **WHEN** a TinyDB record for a resume exists but has no `content_hash` field
- **THEN** the pipeline SHALL treat it as a changed file and perform the in-place update

### Requirement: Deleted resumes are removed from both stores
After processing all PDFs found on disk, the pipeline SHALL identify any resume IDs present in TinyDB but absent from the scanned folder and delete their ChromaDB chunks and TinyDB records.

#### Scenario: Deleted file cleaned up
- **WHEN** a resume ID exists in TinyDB but its PDF is not found in the data folder
- **THEN** the pipeline SHALL delete all ChromaDB chunks for that resume and remove its TinyDB record, and SHALL emit a `"deleted"` event

### Requirement: Progress events extended for update and delete
The pipeline SHALL emit `"updated"` and `"deleted"` event kinds with the same shape as the existing `"done"` and `"skipped"` events respectively. The final `"complete"` event SHALL include `updated` and `deleted` integer counters.

#### Scenario: Complete event includes new counters
- **WHEN** ingestion finishes
- **THEN** the `"complete"` event SHALL contain `updated` (count of re-ingested resumes) and `deleted` (count of removed resumes) in addition to the existing `total`, `skipped`, `errors`, and `categories` fields

### Requirement: Ingestion UI reflects updates and deletions
The Streamlit ingestion tab SHALL display the `updated` and `deleted` counts from the `"complete"` event alongside the existing totals.

#### Scenario: Summary shows all counts
- **WHEN** ingestion completes and the `"complete"` event is received
- **THEN** the success message SHALL include the number of updated and deleted resumes in addition to total processed, skipped, and errors
