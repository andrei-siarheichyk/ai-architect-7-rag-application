## MODIFIED Requirements

### Requirement: Semantic search over resume chunks
The system SHALL allow users to enter a natural language query and retrieve the top-K most semantically similar resume chunks from ChromaDB using `text-embedding-3-small-1` embeddings served by the EPAM DIAL / Azure OpenAI-compatible proxy.

#### Scenario: Successful search returns results
- **WHEN** the user enters a query and clicks Search
- **THEN** the system embeds the query, queries ChromaDB, and displays up to K results each showing resume ID, category, and matched text

#### Scenario: Search with empty ChromaDB
- **WHEN** the user searches but no resumes have been ingested
- **THEN** the system SHALL display a warning prompting the user to run ingestion first

#### Scenario: Search with embedding provider unavailable
- **WHEN** the embedding call to the DIAL / Azure OpenAI proxy fails
- **THEN** the system SHALL display a clear error message and not crash
