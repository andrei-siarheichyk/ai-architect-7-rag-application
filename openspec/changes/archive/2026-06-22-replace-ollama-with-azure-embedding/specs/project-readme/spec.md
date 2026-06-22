## MODIFIED Requirements

### Requirement: Prerequisites section
The README SHALL list all prerequisites a developer needs before running the app: Python version and the EPAM DIAL / Azure OpenAI API key (used for both chat completions and embeddings). The README SHALL NOT require a local Ollama installation or model pull.

#### Scenario: Embedding model called out
- **WHEN** a developer reads the Prerequisites section
- **THEN** the DIAL / Azure OpenAI embedding model `text-embedding-3-small-1` and the required API key SHALL be documented so embeddings work before ingestion, with no `ollama pull` step

### Requirement: Feature descriptions
The README SHALL describe the three main tabs — Ingestion, Search & Ask, and Analytics — and the role-based access control sidebar.

#### Scenario: Ingestion described
- **WHEN** a developer reads the Features section
- **THEN** they SHALL understand that PDF resumes are chunked, embedded via the EPAM DIAL / Azure OpenAI proxy, and stored in ChromaDB

#### Scenario: Search & Ask described
- **WHEN** a developer reads the Features section
- **THEN** they SHALL understand that a single question field triggers vector retrieval followed by streaming LLM Q&A
