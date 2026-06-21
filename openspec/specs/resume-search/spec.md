### Requirement: Semantic search over resume chunks
The system SHALL allow users to enter a natural language query and retrieve the top-K most semantically similar resume chunks from ChromaDB using `nomic-embed-text` embeddings.

#### Scenario: Successful search returns results
- **WHEN** the user enters a query and clicks Search
- **THEN** the system embeds the query, queries ChromaDB, and displays up to K results each showing resume ID, category, and matched text

#### Scenario: Search with empty ChromaDB
- **WHEN** the user searches but no resumes have been ingested
- **THEN** the system SHALL display a warning prompting the user to run ingestion first

#### Scenario: Search with Ollama unavailable
- **WHEN** the embedding call to Ollama fails
- **THEN** the system SHALL display a clear error message and not crash

### Requirement: Configurable result count
The system SHALL provide a slider to configure K (number of results), defaulting to 5 with a range of 1–10.

#### Scenario: User adjusts top-K slider
- **WHEN** the user moves the slider to K=3 and searches
- **THEN** the system SHALL return at most 3 results
