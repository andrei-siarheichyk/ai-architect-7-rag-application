## ADDED Requirements

### Requirement: Single question input drives search and Q&A
The Search tab SHALL present exactly one text input field labelled "Question" and one primary button labelled "Search & Ask". Submitting a non-empty question SHALL trigger vector retrieval followed immediately by streaming LLM Q&A without any additional user interaction.

#### Scenario: User submits a question
- **WHEN** the user types a question and clicks "Search & Ask"
- **THEN** the system retrieves the top-K matching resume chunks and streams an LLM answer on the same page

#### Scenario: Empty question submitted
- **WHEN** the user clicks "Search & Ask" with an empty or whitespace-only input
- **THEN** the system SHALL display a warning and SHALL NOT call the retriever or LLM

### Requirement: Answer precedes chunk display
After a successful "Search & Ask" action the page SHALL render the streamed LLM answer first, then display the retrieved resume chunks as expandable items below it.

#### Scenario: Results displayed after answer
- **WHEN** the LLM answer has finished streaming
- **THEN** a "Results (N)" subheader followed by expandable chunk items SHALL appear beneath the answer

#### Scenario: Source attribution shown
- **WHEN** the answer is displayed
- **THEN** a caption listing unique resume IDs used as sources SHALL appear directly below the answer stream

### Requirement: Role-based access control preserved
The unified action SHALL apply the active role's `allowed_categories` filter during retrieval and PII redaction during chunk display, identical to the previous two-button behaviour.

#### Scenario: Category-scoped retrieval
- **WHEN** the active role has a non-empty `allowed_categories` list
- **THEN** the retriever SHALL be called with that list and only matching chunks SHALL be returned

#### Scenario: PII redaction applied
- **WHEN** chunk text is displayed
- **THEN** the text SHALL be passed through `redact(text, role)` before rendering
