from typing import Generator

from openai import AzureOpenAI

from src.config import OPENAI_API_KEY, OPENAI_MODEL, AZURE_ENDPOINT, AZURE_API_VERSION
from src.access.policy import redact

_client: AzureOpenAI | None = None

_SYSTEM = (
    "You are a helpful assistant. Answer the user's question using ONLY the resume excerpts "
    "provided as context. If the answer is not in the excerpts, say so."
)


def _get_client() -> AzureOpenAI:
    global _client
    if _client is None:
        _client = AzureOpenAI(
            api_key=OPENAI_API_KEY,
            azure_endpoint=AZURE_ENDPOINT,
            api_version=AZURE_API_VERSION,
        )
    return _client


def _build_context(results: list[dict], role: str = "HR") -> str:
    parts = []
    for i, r in enumerate(results, 1):
        text = redact(r["text"], role)
        parts.append(f"[{i}] Resume {r['resume_id']} ({r['category']}):\n{text}")
    print("\n\n".join(parts))
    return "\n\n".join(parts)


def answer_stream(question: str, results: list[dict], role: str = "HR") -> Generator[str, None, None]:
    """Stream an LLM answer grounded in retrieved resume chunks."""
    context = _build_context(results, role)
    user_msg = f"Context:\n{context}\n\nQuestion: {question}"


    stream = _get_client().chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": _SYSTEM},
            {"role": "user", "content": user_msg},
        ],
        stream=True,
    )

    for chunk in stream:
        delta = chunk.choices[0].delta.content if chunk.choices else None
        if delta:
            yield delta
