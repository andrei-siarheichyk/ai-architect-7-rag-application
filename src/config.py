from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"
DB_DIR = ROOT_DIR / "db"
CHROMA_DIR = DB_DIR / "chroma"
TINYDB_PATH = DB_DIR / "resumes.json"

OLLAMA_BASE_URL = "http://localhost:11434"
EMBED_MODEL = "nomic-embed-text"

# EPAM DIAL proxy (Azure OpenAI compatible)
OPENAI_API_KEY = "your-key-here"
OPENAI_MODEL = "gpt-4o" #"claude-sonnet-4-5@20250929" #"gpt-4.1-mini-2025-04-14"
AZURE_ENDPOINT = "https://ai-proxy.lab.epam.com"
AZURE_API_VERSION = "2023-07-01-preview"

CHUNK_SIZE = 512
CHUNK_OVERLAP = 50
