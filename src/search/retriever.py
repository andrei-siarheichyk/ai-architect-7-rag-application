import chromadb
from openai import AzureOpenAI

from src.config import CHROMA_DIR, EMBED_MODEL, OPENAI_API_KEY, AZURE_ENDPOINT, AZURE_API_VERSION

_client: AzureOpenAI | None = None
_collection = None


def _get_client() -> AzureOpenAI:
    global _client
    if _client is None:
        _client = AzureOpenAI(
            api_key=OPENAI_API_KEY,
            azure_endpoint=AZURE_ENDPOINT,
            api_version=AZURE_API_VERSION,
        )
    return _client


def _get_collection():
    global _collection
    if _collection is None:
        client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        _collection = client.get_or_create_collection("resumes")
    return _collection


def collection_count() -> int:
    try:
        return _get_collection().count()
    except Exception:
        return 0


def search(query: str, top_k: int = 5, allowed_categories: list[str] | None = None) -> list[dict]:
    """Embed query and return top-K matching chunks from ChromaDB."""
    embedding = _get_client().embeddings.create(model=EMBED_MODEL, input=[query]).data[0].embedding
    where = {"category": {"$in": allowed_categories}} if allowed_categories else None
    results = _get_collection().query(
        query_embeddings=[embedding],
        n_results=top_k,
        where=where,
        include=["documents", "metadatas", "distances"],
    )

    hits = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        hits.append({
            "resume_id": meta.get("resume_id", ""),
            "category": meta.get("category", ""),
            "text": doc,
            "distance": round(dist, 4),
        })
    return hits
