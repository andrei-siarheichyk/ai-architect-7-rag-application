## ADDED Requirements

### Requirement: IVectorStore interface
The system SHALL define an `IVectorStore` interface with `UpsertAsync` and `SearchAsync` methods, enabling Phase 2 swap to Qdrant without changing callers.

#### Scenario: Interface contract
- **WHEN** `InMemoryVectorStore` is injected as `IVectorStore`
- **THEN** `Retriever` and `IngestionPipeline` SHALL work without knowing the concrete implementation

### Requirement: In-memory cosine similarity search
The system SHALL implement `InMemoryVectorStore` storing `List<VectorEntry>` and computing cosine similarity to find top-K nearest neighbours.

#### Scenario: Search returns top-K by similarity
- **WHEN** `SearchAsync(queryVector, topK: 5)` is called
- **THEN** the store SHALL return the 5 entries with highest cosine similarity to the query vector, sorted descending

#### Scenario: Category filter applied
- **WHEN** `SearchAsync` is called with `allowedCategories: ["ENGINEERING"]`
- **THEN** only entries whose metadata category matches SHALL be considered

#### Scenario: Store is empty
- **WHEN** no vectors have been upserted
- **THEN** `SearchAsync` SHALL return an empty list without throwing

### Requirement: LiteDB document store
The system SHALL use LiteDB to persist `Resume` records keyed by `ResumeId`. Upsert SHALL insert or replace.

#### Scenario: Upsert new resume
- **WHEN** `DocumentStore.Upsert(resume)` is called with a new `ResumeId`
- **THEN** the document SHALL be inserted into LiteDB

#### Scenario: Upsert existing resume
- **WHEN** `DocumentStore.Upsert(resume)` is called with an existing `ResumeId`
- **THEN** the existing document SHALL be replaced
