import chromadb
from llama_index.embeddings.ollama import OllamaEmbedding

from src.config import CHROMA_DIR, EMBED_MODEL, OLLAMA_BASE_URL

_embed_model: OllamaEmbedding | None = None
_collection = None


def _get_embed_model() -> OllamaEmbedding:
    global _embed_model
    if _embed_model is None:
        _embed_model = OllamaEmbedding(
            model_name=EMBED_MODEL,
            base_url=OLLAMA_BASE_URL,
        )
    return _embed_model


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
    embedding = _get_embed_model().get_text_embedding(query)
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
