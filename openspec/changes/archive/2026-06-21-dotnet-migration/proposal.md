## Why

The existing Python implementation works but .NET is the developer's primary stack. Porting the project to C# makes the RAG pipeline easier to read, extend, and reason about — and is a deliberate learning exercise in how RAG concepts (chunking, embedding, vector search, structured extraction, retrieval-augmented generation) translate to idiomatic .NET code with no magic abstractions hiding the steps.

## What Changes

- Create a new `ResumeRag/` .NET 8 console project alongside the existing Python code (not a replacement — both live in the repo)
- Re-implement all 9 Python modules as C# classes with a 1:1 mapping
- Use direct HTTP calls to Ollama (no Semantic Kernel) so every embedding and LLM call is visible
- Use in-memory cosine similarity for vector search in Phase 1 (learning); designed so `VectorStore.cs` can be swapped to Qdrant in Phase 2
- Use LiteDB as the structured document store (equivalent of TinyDB)
- Use PdfPig for PDF text extraction (equivalent of PyMuPDF)
- Use `Azure.AI.OpenAI` SDK for structured extraction and Q&A via EPAM DIAL proxy
- Console app UI: menu-driven, prints each pipeline step so the learner sees what's happening

## Capabilities

### New Capabilities
- `dotnet-pdf-extractor`: PdfPig-based PDF text extraction, mirrors `extractor.py`
- `dotnet-text-chunker`: hand-rolled sliding window chunker + Ollama embedding via HttpClient, mirrors `chunker.py`
- `dotnet-structured-extractor`: AzureOpenAI JSON extraction to C# record + LiteDB persistence, mirrors `structured.py`
- `dotnet-ingestion-pipeline`: orchestrates extractor → chunker → structured extractor with console progress output, mirrors `pipeline.py`
- `dotnet-vector-store`: in-memory vector store with cosine similarity search, mirrors ChromaDB usage
- `dotnet-retriever`: embeds query via Ollama, searches vector store with role-based category filter, mirrors `retriever.py`
- `dotnet-qa-service`: builds context from results, streams answer via AzureOpenAI, mirrors `qa.py`
- `dotnet-aggregator`: LINQ aggregations over LiteDB documents (skill frequency, seniority, experience), mirrors `aggregator.py`
- `dotnet-access-policy`: role policies + PII redaction via regex, mirrors `policy.py`

### Modified Capabilities
- *(none — this is a parallel implementation, not a modification of the Python app)*

## Impact

- New directory: `ResumeRag/` (.NET 8 console project)
- No changes to existing Python code
- Shares the same `/data` folder of PDF resumes
- Separate `db/` for .NET stores: `ResumeRag/db/resumes.db` (LiteDB), in-memory vectors (reset on each run in Phase 1)
- Dependencies: `PdfPig`, `LiteDB`, `Azure.AI.OpenAI`, `Microsoft.Extensions.Http`
- Requires: Ollama running on `localhost:11434`, EPAM DIAL API key in environment
