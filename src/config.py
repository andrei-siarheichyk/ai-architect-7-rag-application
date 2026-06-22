from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"
DB_DIR = ROOT_DIR / "db"
CHROMA_DIR = DB_DIR / "chroma"
TINYDB_PATH = DB_DIR / "resumes.json"

EMBED_MODEL = "text-embedding-3-small-1"

# EPAM DIAL proxy (Azure OpenAI compatible) — used for chat completions and embeddings
OPENAI_API_KEY = ""
OPENAI_MODEL = "gpt-4o" #"claude-sonnet-4-5@20250929" #"gpt-4.1-mini-2025-04-14"
AZURE_ENDPOINT = "https://ai-proxy.lab.epam.com"
AZURE_API_VERSION = "2023-07-01-preview"

CHUNK_SIZE = 512
CHUNK_OVERLAP = 50
