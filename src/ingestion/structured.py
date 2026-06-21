import json
import logging
from datetime import datetime, timezone

from openai import AzureOpenAI
from tinydb import TinyDB, Query

from src.config import TINYDB_PATH, OPENAI_API_KEY, OPENAI_MODEL, AZURE_ENDPOINT, AZURE_API_VERSION

logger = logging.getLogger(__name__)

_client: AzureOpenAI | None = None

_SYSTEM = (
    "You are a resume parser. Extract structured fields and return ONLY valid JSON. "
    "No explanation, no markdown."
)

_PROMPT = """Extract the following fields from this resume and return a JSON object:
- "skills": list of strings (skills and technologies)
- "years_exp": integer (total years of work experience, 0 if unknown)
- "education": string (highest degree and field, empty string if unknown)
- "job_titles": list of strings (job titles held)
- "certifications": list of strings (empty list if none)

Resume:
{text}
"""

_EMPTY = {"skills": [], "years_exp": 0, "education": "", "job_titles": [], "certifications": []}


def _get_client() -> AzureOpenAI:
    global _client
    if _client is None:
        _client = AzureOpenAI(
            api_key=OPENAI_API_KEY,
            azure_endpoint=AZURE_ENDPOINT,
            api_version=AZURE_API_VERSION,
        )
    return _client


def extract_structured(resume_id: str, category: str, text: str, chunk_count: int, content_hash: str = "") -> dict:
    """Extract structured fields via OpenAI and persist to TinyDB."""
    try:
        response = _get_client().chat.completions.create(
            model=OPENAI_MODEL,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": _SYSTEM},
                {"role": "user", "content": _PROMPT.format(text=text[:3000])},
            ],
        )
        fields = json.loads(response.choices[0].message.content)
    except Exception as e:
        logger.warning(f"Structured extraction failed for {resume_id}: {e}")
        fields = {}

    doc = {
        "resume_id": resume_id,
        "category": category,
        "skills": fields.get("skills", _EMPTY["skills"]),
        "years_exp": fields.get("years_exp", _EMPTY["years_exp"]),
        "education": fields.get("education", _EMPTY["education"]),
        "job_titles": fields.get("job_titles", _EMPTY["job_titles"]),
        "certifications": fields.get("certifications", _EMPTY["certifications"]),
        "chunk_count": chunk_count,
        "content_hash": content_hash,
        "ingested_at": datetime.now(timezone.utc).isoformat(),
    }

    TINYDB_PATH.parent.mkdir(parents=True, exist_ok=True)
    db = TinyDB(str(TINYDB_PATH))
    db.upsert(doc, Query().resume_id == resume_id)

    return doc
