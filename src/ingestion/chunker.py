import chromadb
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.schema import Document
from llama_index.embeddings.ollama import OllamaEmbedding

from src.config import CHROMA_DIR, EMBED_MODEL, OLLAMA_BASE_URL, CHUNK_SIZE, CHUNK_OVERLAP

_embed_model: OllamaEmbedding | None = None
_chroma_collection = None


def _get_embed_model() -> OllamaEmbedding:
    global _embed_model
    if _embed_model is None:
        _embed_model = OllamaEmbedding(
            model_name=EMBED_MODEL,
            base_url=OLLAMA_BASE_URL,
        )
    return _embed_model


def _get_collection():
    global _chroma_collection
    if _chroma_collection is None:
        CHROMA_DIR.mkdir(parents=True, exist_ok=True)
        client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        _chroma_collection = client.get_or_create_collection("resumes")
    return _chroma_collection


def delete_chunks(resume_id: str, chunk_count: int) -> None:
    """Remove all ChromaDB chunks for a resume by their deterministic IDs."""
    _get_collection().delete(ids=[f"{resume_id}_{i}" for i in range(chunk_count)])


def chunk_and_store(resume_id: str, category: str, text: str) -> int:
    """Split text into chunks, embed, and store in ChromaDB. Returns chunk count."""
    splitter = SentenceSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    nodes = splitter.get_nodes_from_documents([Document(text=text)])
    if not nodes:
        return 0

    texts = [node.get_content() for node in nodes]
    total = len(texts)

    embeddings = _get_embed_model().get_text_embedding_batch(texts)
    collection = _get_collection()

    collection.add(
        ids=[f"{resume_id}_{i}" for i in range(total)],
        documents=texts,
        embeddings=embeddings,
        metadatas=[
            {"resume_id": resume_id, "category": category, "chunk_index": i, "total_chunks": total}
            for i in range(total)
        ],
    )
    return total
