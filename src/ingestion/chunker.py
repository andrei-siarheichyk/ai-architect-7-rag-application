import chromadb
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.schema import Document
from openai import AzureOpenAI

from src.config import (
    CHROMA_DIR,
    EMBED_MODEL,
    OPENAI_API_KEY,
    AZURE_ENDPOINT,
    AZURE_API_VERSION,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
)

_client: AzureOpenAI | None = None
_chroma_collection = None


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

    response = _get_client().embeddings.create(model=EMBED_MODEL, input=texts)
    embeddings = [item.embedding for item in sorted(response.data, key=lambda d: d.index)]
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
