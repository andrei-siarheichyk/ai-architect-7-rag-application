## Context

The Python app has 9 source files (~650 LOC) across 4 modules (ingestion, search, analytics, access) plus a Streamlit UI. Each file maps to one C# class. The goal is transparent learning: every RAG step should be a readable method call, not a framework abstraction.

## Goals / Non-Goals

**Goals:**
- 1:1 Python → C# file mapping so learner can compare implementations side-by-side
- No Semantic Kernel — direct HttpClient calls to Ollama so embedding and LLM calls are visible
- In-memory vector store in Phase 1 — implement cosine similarity in C# to understand what vector DBs do
- Console app UI that prints each pipeline step: "Extracted 3 pages", "Created 7 chunks", "Embedded", "Stored"
- Idiomatic C# 12 / .NET 8: records, pattern matching, async/await throughout

**Non-Goals:**
- Replacing the Python app
- Web UI (console first, add ASP.NET Core later when pipeline is understood)
- Qdrant integration (Phase 2 upgrade, not in scope here)
- Re-ingesting into Python's ChromaDB (separate .NET stores)

## Decisions

**No Semantic Kernel**
SK abstracts chunking, embedding, and retrieval into single calls. For learning, each step must be a separate, readable operation. Direct HttpClient → Ollama makes the embedding API call visible; implementing cosine similarity makes vector search tangible.

**In-memory vector store over Qdrant**
Phase 1 stores `List<VectorEntry>` in memory. `VectorStore.SearchAsync` loops through entries computing cosine similarity. This is O(n) and breaks at scale, but it teaches exactly what Qdrant does internally. The `IVectorStore` interface allows swapping to Qdrant without changing any other code.

**LiteDB over SQLite or EF Core**
TinyDB stores schema-less JSON documents. LiteDB is the closest .NET equivalent — embedded, no server, stores C# objects directly as BSON. No migrations, no ORM. Maps to TinyDB's `upsert` pattern with `GetCollection<Resume>().Upsert(doc)`.

**Azure.AI.OpenAI SDK over raw HttpClient for LLM**
Ollama is called via raw HttpClient (learning value). AzureOpenAI is called via the official SDK — the EPAM DIAL proxy is Azure-compatible and the SDK handles streaming cleanly with `CompleteChatStreamingAsync`. The SDK call is still one readable line, not a black box.

**Console menu UI**
Removes all UI concerns from the learning scope. The pipeline logic is the learning target. `Program.cs` is a simple `while(true)` menu: Ingest / Search / Ask / Analytics / Switch Role.

## Project structure

```
ResumeRag/
├── ResumeRag.csproj
├── Program.cs                     # console menu
├── AppConfig.cs                   # paths, URLs, model names
│
├── Models/
│   ├── Resume.cs                  # LiteDB document
│   ├── ResumeChunk.cs             # vector store entry
│   └── SearchResult.cs            # retriever output
│
├── Ingestion/
│   ├── PdfExtractor.cs            # PdfPig → string
│   ├── TextChunker.cs             # sliding window → List<string>
│   ├── EmbeddingService.cs        # Ollama /api/embed → float[]
│   ├── StructuredExtractor.cs     # AzureOpenAI → Resume fields
│   └── IngestionPipeline.cs       # orchestrator
│
├── Storage/
│   ├── IVectorStore.cs            # interface (swap in Qdrant later)
│   ├── InMemoryVectorStore.cs     # cosine similarity implementation
│   └── DocumentStore.cs          # LiteDB wrapper
│
├── Search/
│   ├── Retriever.cs               # embed query + IVectorStore.Search
│   └── QaService.cs               # context + streaming LLM
│
├── Analytics/
│   └── Aggregator.cs              # LINQ over LiteDB
│
└── Access/
    └── Policy.cs                  # POLICIES dict + Redact()
```

## Key C# patterns

**Ollama embedding call (EmbeddingService.cs)**
```csharp
var body = JsonSerializer.Serialize(new { model = "nomic-embed-text", input = text });
var resp = await _http.PostAsync(".../api/embed", new StringContent(body, ...));
var json = await JsonSerializer.DeserializeAsync<OllamaEmbedResponse>(resp.Content...);
return json.Embeddings[0];  // float[]
```

**Cosine similarity (InMemoryVectorStore.cs)**
```csharp
static float Cosine(float[] a, float[] b) {
    var dot  = a.Zip(b, (x, y) => x * y).Sum();
    var magA = MathF.Sqrt(a.Sum(x => x * x));
    var magB = MathF.Sqrt(b.Sum(x => x * x));
    return dot / (magA * magB);
}
```

**LINQ aggregation (Aggregator.cs)**
```csharp
resumes.SelectMany(r => r.Skills)
       .GroupBy(s => s, StringComparer.OrdinalIgnoreCase)
       .OrderByDescending(g => g.Count())
       .Take(topN)
       .Select(g => (g.Key, g.Count()))
```

## Risks / Trade-offs

- **In-memory store resets on exit** → re-ingest on each run until Phase 2 Qdrant upgrade; acceptable for learning
- **Ollama call is synchronous-feeling** → use `async/await` throughout; `HttpClient` is async natively
- **LiteDB has no async API** → wrap in `Task.Run` for non-blocking console ops; acceptable trade-off
