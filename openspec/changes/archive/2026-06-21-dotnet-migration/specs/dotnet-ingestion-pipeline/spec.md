## ADDED Requirements

### Requirement: PDF text extraction
The system SHALL extract plain text from PDF files using PdfPig, walking the `/data/<CATEGORY>/<ID>.pdf` folder structure and yielding `(resumeId, category, text)` tuples.

#### Scenario: Successful extraction
- **WHEN** a valid PDF exists at `data/ENGINEERING/12345.pdf`
- **THEN** `PdfExtractor.Extract()` SHALL return non-empty text and derive `resumeId = "12345"`, `category = "ENGINEERING"`

#### Scenario: Empty or unreadable PDF
- **WHEN** a PDF yields no extractable text
- **THEN** the extractor SHALL log a warning and skip that file without throwing

### Requirement: Sliding window text chunking
The system SHALL split resume text into overlapping chunks using a sliding window of configurable size (default 512 tokens/chars) and overlap (default 50).

#### Scenario: Text shorter than chunk size
- **WHEN** extracted text is shorter than the chunk size
- **THEN** `TextChunker.Chunk()` SHALL return a single chunk containing the full text

#### Scenario: Text longer than chunk size
- **WHEN** extracted text spans multiple chunks
- **THEN** consecutive chunks SHALL overlap by the configured overlap amount

### Requirement: Ollama embedding via HttpClient
The system SHALL embed text by calling `POST localhost:11434/api/embed` directly via `HttpClient`, returning a `float[]` vector.

#### Scenario: Successful embedding
- **WHEN** Ollama is running and `nomic-embed-text` is available
- **THEN** `EmbeddingService.EmbedAsync(text)` SHALL return a non-empty `float[]`

#### Scenario: Ollama unavailable
- **WHEN** Ollama is not running
- **THEN** the service SHALL throw a descriptive exception that surfaces in the console

### Requirement: Structured field extraction via AzureOpenAI
The system SHALL send truncated resume text to `gpt-4o-2024-11-20` via EPAM DIAL and deserialize the JSON response into a `Resume` record with fields: `Skills`, `YearsExp`, `Education`, `JobTitles`, `Certifications`.

#### Scenario: Successful extraction
- **WHEN** the LLM returns valid JSON
- **THEN** `StructuredExtractor.ExtractAsync()` SHALL return a populated `Resume` record

#### Scenario: Malformed JSON response
- **WHEN** the LLM returns unparseable output
- **THEN** the extractor SHALL return a `Resume` record with empty/default fields and log a warning

### Requirement: Idempotent ingestion pipeline
The system SHALL skip resumes already present in LiteDB, allowing safe re-runs. The pipeline SHALL print progress to the console for each resume processed.

#### Scenario: Resume already ingested
- **WHEN** a `resumeId` already exists in LiteDB
- **THEN** the pipeline SHALL print "Skipped: {resumeId}" and continue

#### Scenario: Fresh ingestion
- **WHEN** a resume is not in LiteDB
- **THEN** the pipeline SHALL print each step: "Extracted", "Chunked (N)", "Embedded", "Stored"
