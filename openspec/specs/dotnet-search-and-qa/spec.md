### Requirement: Semantic retrieval with role-based category filter
The system SHALL embed the user query via Ollama and search `IVectorStore`, applying the active role's `AllowedCategories` filter. Returns `List<SearchResult>`.

#### Scenario: HR role returns all categories
- **WHEN** role is HR and query is submitted
- **THEN** results SHALL include chunks from any category

#### Scenario: Hiring Manager role filters to Engineering and IT
- **WHEN** role is Hiring Manager and query is submitted
- **THEN** results SHALL only include chunks from ENGINEERING and INFORMATION-TECHNOLOGY

### Requirement: Streaming Q&A via AzureOpenAI
The system SHALL build a prompt from retrieved chunks, call `CompleteChatStreamingAsync` on the EPAM DIAL endpoint, and stream tokens to the console as they arrive.

#### Scenario: Streaming answer printed token by token
- **WHEN** `QaService.StreamAnswerAsync(question, results, role)` is called
- **THEN** each token SHALL be written to `Console.Write` as it arrives, without buffering

#### Scenario: PII redaction for Recruiter role
- **WHEN** role is Recruiter and results contain email addresses
- **THEN** the context passed to the LLM SHALL have emails replaced with `[EMAIL REDACTED]`

#### Scenario: No results available
- **WHEN** the vector store returns an empty result set
- **THEN** `QaService` SHALL print "No results found for this query" and skip the LLM call
