### Requirement: Natural language Q&A over retrieved chunks
The system SHALL allow users to ask a question about the search results, sending retrieved chunks as context to `gpt-4o-2024-11-20` via EPAM DIAL and streaming the answer back.

#### Scenario: Successful Q&A answer
- **WHEN** the user types a question and clicks Ask after a search
- **THEN** the system SHALL stream the LLM answer token-by-token and display source resume IDs below the answer

#### Scenario: Q&A without prior search
- **WHEN** the user clicks Ask without having performed a search first
- **THEN** the system SHALL display a message asking the user to search first

#### Scenario: LLM call fails
- **WHEN** the EPAM DIAL API returns an error
- **THEN** the system SHALL display the error message and not crash

### Requirement: Source attribution
The system SHALL display the resume IDs used as context sources below every LLM answer.

#### Scenario: Sources shown after answer
- **WHEN** the LLM answer is complete
- **THEN** the system SHALL list the resume IDs of all chunks used as context
