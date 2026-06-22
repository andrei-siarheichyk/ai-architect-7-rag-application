## Purpose

Generating embedding vectors for text via the EPAM DIAL / Azure OpenAI-compatible proxy, shared by the ingestion and search paths so stored and query vectors live in the same space.

## ADDED Requirements

### Requirement: Embedding generation via DIAL / Azure OpenAI proxy
The system SHALL generate text embedding vectors by calling the EPAM DIAL / Azure OpenAI-compatible embeddings endpoint with model `text-embedding-3-small-1`, authenticated with the same `OPENAI_API_KEY`, `AZURE_ENDPOINT`, and `AZURE_API_VERSION` configuration used for chat completions. The system SHALL NOT depend on a local Ollama service for embeddings.

#### Scenario: Single text embedded
- **WHEN** a caller requests an embedding for one piece of text
- **THEN** the system SHALL return a single vector produced by the `text-embedding-3-small-1` model via the DIAL proxy

#### Scenario: Batch of texts embedded
- **WHEN** the ingestion pipeline submits a list of chunk texts in one request
- **THEN** the system SHALL return one vector per input, in the same order as the inputs

#### Scenario: Embedding provider unavailable
- **WHEN** the embedding request to the DIAL proxy fails (network, auth, or rate limit)
- **THEN** the system SHALL surface a clear error rather than storing or querying with an empty or partial vector

### Requirement: Shared embedding configuration for ingestion and search
The system SHALL use the same embedding model and endpoint for both ingestion (storing resume chunks) and search (embedding queries) so that stored vectors and query vectors share the same vector space.

#### Scenario: Query embedding matches stored embedding space
- **WHEN** a query is embedded for retrieval
- **THEN** it SHALL be produced by the same `text-embedding-3-small-1` model used during ingestion, yielding vectors of matching dimensionality for ChromaDB similarity search
