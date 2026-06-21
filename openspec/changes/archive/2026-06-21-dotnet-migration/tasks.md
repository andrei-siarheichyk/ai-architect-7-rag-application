## 1. Project Scaffolding

- [x] 1.1 Create `ResumeRag/ResumeRag.csproj` (.NET 8 console app) with packages: `PdfPig`, `LiteDB`, `Azure.AI.OpenAI`, `Microsoft.Extensions.Http`
- [x] 1.2 Create `ResumeRag/AppConfig.cs` with constants: `DataDir`, `DbPath`, `OllamaBaseUrl`, `EmbedModel`, `LlmModel`, `AzureEndpoint`, `AzureApiVersion`, `ChunkSize`, `ChunkOverlap`
- [x] 1.3 Create `ResumeRag/Models/Resume.cs` (LiteDB document: `ResumeId`, `Category`, `Skills`, `YearsExp`, `Education`, `JobTitles`, `Certifications`, `ChunkCount`, `IngestedAt`), `ResumeChunk.cs` (vector entry: `Id`, `ResumeId`, `Category`, `Text`, `Vector`), `SearchResult.cs` (`ResumeId`, `Category`, `Text`, `Score`)

## 2. Ingestion — PDF + Chunking + Embedding

- [x] 2.1 Create `ResumeRag/Ingestion/PdfExtractor.cs`: static `IEnumerable<(string resumeId, string category, string text)> ExtractAll(string dataDir)` — walk directory, open each PDF with PdfPig, concatenate page text
- [x] 2.2 Create `ResumeRag/Ingestion/TextChunker.cs`: static `List<string> Chunk(string text, int size, int overlap)` — sliding window chunker, returns list of text chunks
- [x] 2.3 Create `ResumeRag/Ingestion/EmbeddingService.cs`: `Task<float[]> EmbedAsync(string text)` and `Task<List<float[]>> EmbedBatchAsync(List<string> texts)` — call `POST {OllamaBaseUrl}/api/embed` via injected `HttpClient`, deserialize response

## 3. Storage

- [x] 3.1 Create `ResumeRag/Storage/IVectorStore.cs`: interface with `Task UpsertAsync(string resumeId, string category, List<string> chunks, List<float[]> vectors)` and `Task<List<SearchResult>> SearchAsync(float[] query, int topK, List<string>? allowedCategories)`
- [x] 3.2 Create `ResumeRag/Storage/InMemoryVectorStore.cs`: implement `IVectorStore` with `List<ResumeChunk>` backing store and static `float CosineSimilarity(float[] a, float[] b)` helper
- [x] 3.3 Create `ResumeRag/Storage/DocumentStore.cs`: LiteDB wrapper with `Upsert(Resume doc)`, `bool Exists(string resumeId)`, `List<Resume> GetAll()`, `List<Resume> GetByCategories(List<string> categories)`

## 4. Ingestion — Structured Extraction + Pipeline

- [x] 4.1 Create `ResumeRag/Ingestion/StructuredExtractor.cs`: `Task<Resume> ExtractAsync(string resumeId, string category, string text)` — call AzureOpenAI with JSON mode prompt, deserialize to `Resume`, persist to `DocumentStore`
- [x] 4.2 Create `ResumeRag/Ingestion/IngestionPipeline.cs`: `Task RunAsync(string dataDir)` — for each PDF: check `DocumentStore.Exists` → skip or extract → chunk → embed batch → vector store upsert → structured extract → print step-by-step progress

## 5. Search + Q&A

- [x] 5.1 Create `ResumeRag/Search/Retriever.cs`: `Task<List<SearchResult>> SearchAsync(string query, int topK, string role)` — embed query, get `AllowedCategories` from policy, call `IVectorStore.SearchAsync`
- [x] 5.2 Create `ResumeRag/Search/QaService.cs`: `Task StreamAnswerAsync(string question, List<SearchResult> results, string role)` — apply `Policy.Redact` to each chunk, build context string, call `CompleteChatStreamingAsync`, write tokens to `Console.Write` as they arrive

## 6. Analytics + Access

- [x] 6.1 Create `ResumeRag/Analytics/Aggregator.cs`: `List<(string Skill, int Count)> SkillFrequency(int topN, List<string>? allowedCategories)`, `Dictionary<string, int> SeniorityDistribution(List<string>? allowedCategories)`, `List<int> ExperienceValues(List<string>? allowedCategories)` — all using LINQ over `DocumentStore.GetAll()`
- [x] 6.2 Create `ResumeRag/Access/Policy.cs`: static `POLICIES` dictionary, `PolicyEntry Get(string role)`, `string Redact(string text, string role)` with Regex for email, phone, address

## 7. Console UI

- [x] 7.1 Create `ResumeRag/Program.cs`: `while(true)` menu loop showing active role in header; options: (1) Ingest, (2) Search, (3) Ask, (4) Analytics, (5) Switch Role, (0) Exit; wire all services together using manual DI (no IoC container needed)
