import fitz  # PyMuPDF
import logging
from pathlib import Path
from typing import Iterator

logger = logging.getLogger(__name__)


def extract_resumes(data_dir: str) -> Iterator[tuple[str, str, str]]:
    """Walk data_dir/<Category>/<ID>.pdf and yield (resume_id, category, text)."""
    root = Path(data_dir)
    for pdf_path in sorted(root.rglob("*.pdf")):
        resume_id = pdf_path.stem
        category = pdf_path.parent.name
        try:
            doc = fitz.open(str(pdf_path))
            text = "\n".join(page.get_text() for page in doc)
            doc.close()
            if not text.strip():
                logger.warning(f"No text extracted from {pdf_path}")
                continue
            yield resume_id, category, text
        except Exception as e:
            logger.warning(f"Failed to extract {pdf_path}: {e}")


def count_pdfs(data_dir: str) -> int:
    return len(list(Path(data_dir).rglob("*.pdf")))
