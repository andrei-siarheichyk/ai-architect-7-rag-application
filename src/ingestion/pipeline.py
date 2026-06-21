import hashlib
from typing import Generator

from tinydb import TinyDB, Query

from src.config import TINYDB_PATH
from src.ingestion.extractor import extract_resumes
from src.ingestion.chunker import chunk_and_store, delete_chunks
from src.ingestion.structured import extract_structured


def _text_hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def run_ingestion(data_dir: str) -> Generator[dict, None, None]:
    """
    Yield progress events for each resume, then a final summary.

    Event shapes:
      {"status": "skipped",  "resume_id": ..., "processed": int, "total": int}
      {"status": "done",     "resume_id": ..., "category": ..., "chunk_count": int, "processed": int, "total": int}
      {"status": "updated",  "resume_id": ..., "category": ..., "chunk_count": int, "processed": int, "total": int}
      {"status": "deleted",  "resume_id": ..., "processed": int, "total": int}
      {"status": "error",    "resume_id": ..., "error": str,    "processed": int, "total": int}
      {"status": "complete", "total": int, "skipped": int, "updated": int, "deleted": int, "errors": int, "categories": {category: count}}
    """
    TINYDB_PATH.parent.mkdir(parents=True, exist_ok=True)
    db = TinyDB(str(TINYDB_PATH))
    resume_query = Query()

    # Build a dict of existing records for O(1) lookup
    existing_records: dict[str, dict] = {r["resume_id"]: r for r in db.all()}

    # collect all resume paths upfront so we can report total
    all_resumes = list(extract_resumes(data_dir))
    total = len(all_resumes)

    processed = 0
    skipped = 0
    updated = 0
    errors = 0
    categories: dict[str, int] = {}
    seen_on_disk: set[str] = set()

    for resume_id, category, text in all_resumes:
        processed += 1
        seen_on_disk.add(resume_id)
        current_hash = _text_hash(text)
        existing = existing_records.get(resume_id)

        if existing and existing.get("content_hash") == current_hash:
            skipped += 1
            yield {"status": "skipped", "resume_id": resume_id, "processed": processed, "total": total}
            continue

        # Delete stale chunks and record if this is an update
        is_update = existing is not None
        if is_update:
            try:
                delete_chunks(resume_id, existing["chunk_count"])
            except Exception:
                pass
            db.remove(resume_query.resume_id == resume_id)

        try:
            chunk_count = chunk_and_store(resume_id, category, text)
            extract_structured(resume_id, category, text, chunk_count, content_hash=current_hash)
            categories[category] = categories.get(category, 0) + 1
            if is_update:
                updated += 1
                yield {"status": "updated", "resume_id": resume_id, "category": category,
                       "chunk_count": chunk_count, "processed": processed, "total": total}
            else:
                yield {"status": "done", "resume_id": resume_id, "category": category,
                       "chunk_count": chunk_count, "processed": processed, "total": total}
        except Exception as e:
            errors += 1
            yield {"status": "error", "resume_id": resume_id, "error": str(e),
                   "processed": processed, "total": total}

    # Orphan sweep: remove resumes that exist in DB but are gone from disk
    orphaned = set(existing_records.keys()) - seen_on_disk
    deleted = 0
    for resume_id in orphaned:
        record = existing_records[resume_id]
        try:
            delete_chunks(resume_id, record["chunk_count"])
        except Exception:
            pass
        db.remove(resume_query.resume_id == resume_id)
        deleted += 1
        yield {"status": "deleted", "resume_id": resume_id,
               "processed": total, "total": total}

    yield {
        "status": "complete",
        "total": total,
        "skipped": skipped,
        "updated": updated,
        "deleted": deleted,
        "errors": errors,
        "categories": categories,
    }
