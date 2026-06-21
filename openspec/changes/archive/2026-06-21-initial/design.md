# Design — Ingestion Pipeline

## Project structure

```
rag-creation/
├── data/                        # Kaggle dataset (user-provided)
│   ├── Finance/
│   │   └── 16852740.pdf
│   ├── Engineering/
│   └── ...
├── db/
│   ├── chroma/                  # ChromaDB persistent store
│   └── resumes.json             # TinyDB file
├── src/
│   ├── config.py                # paths, Ollama URLs, chunk settings
│   └── ingestion/
│       ├── __init__.py
│       ├── extractor.py         # PyMuPDF: PDF → (resume_id, category, text)
│       ├── chunker.py           # LlamaIndex: text → chunks → ChromaDB
│       ├── structured.py        # Qwen3: text → structured fields → TinyDB
│       └── pipeline.py          # orchestrates extractor + chunker + structured
├── app.py                       # Streamlit entry point
└── requirements.txt
```

## Data flow

```
/data/<Category>/<ID>.pdf
        │
        ▼
  extractor.py  (PyMuPDF)
  → resume_id = filename stem
  → category  = parent folder name
  → text      = full extracted text
        │
        ├──────────────────────────────────┐
        ▼                                  ▼
  chunker.py                         structured.py
  SentenceSplitter(512, overlap=50)  Qwen3 prompt → JSON
  OllamaEmbedding(nomic-embed-text)  parse → TinyDB document
  → ChromaDB collection "resumes"
    metadata: resume_id, category,
              chunk_index, total_chunks
```

## ChromaDB schema

Collection name: `resumes`

```
document  : chunk text
embedding : nomic-embed-text vector
metadata  : {
  resume_id    : str   # "16852740"
  category     : str   # "Finance"
  chunk_index  : int   # 0, 1, 2 ...
  total_chunks : int
}
id        : "{resume_id}_{chunk_index}"
```

## TinyDB schema

```json
{
  "resume_id":    "16852740",
  "category":     "Finance",
  "skills":       ["Excel", "Bloomberg", "Python", "SAP"],
  "years_exp":    7,
  "education":    "Master's in Finance",
  "job_titles":   ["Financial Analyst", "Senior Analyst"],
  "certifications": ["CFA Level 1"],
  "chunk_count":  4,
  "ingested_at":  "2026-06-13T12:00:00Z"
}
```

## Qwen3 extraction prompt (structured.py)

```
Extract the following fields from this resume text and return ONLY valid JSON.
No explanation, no markdown fences, no thinking.

Fields:
- skills: list of skills and technologies (strings)
- years_exp: total years of work experience (integer, 0 if unknown)
- education: highest degree and field (string)
- job_titles: list of job titles held (strings)
- certifications: list of certifications (strings, empty list if none)

Resume:
{text}
```

Note: prepend `/no_think` to suppress Qwen3 thinking mode.

## Idempotency

Before processing a PDF, check TinyDB for existing `resume_id`.
If found, skip both chunker and structured extraction.
This allows safe re-runs and incremental ingestion.

## Streamlit UI (app.py)

```
[ Data folder path: _____________ ]  [ Start Ingestion ]

Ingesting resumes...
████████████░░░░░░░░  247 / 2400

✓ Finance         48 resumes
✓ Engineering     52 resumes
⟳ Banking         ...

Done: 2400 resumes | 9,847 chunks | 24 categories
```
