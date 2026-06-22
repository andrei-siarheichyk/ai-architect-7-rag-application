# Resume Analyzer — RAG Application

A Retrieval-Augmented Generation (RAG) application that ingests PDF resumes, enables semantic search and natural-language Q&A over them, and visualizes workforce analytics. Built with **LlamaIndex**, **ChromaDB**, the **EPAM DIAL / Azure OpenAI proxy**, and **Streamlit**.

---

## Dataset

Resume PDFs are organized by job category under `data/`:

```
data/
  ENGINEERING/           # Software / hardware engineering resumes
  INFORMATION-TECHNOLOGY/  # IT roles
```

Source: [Kaggle — Resume Dataset](https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset) (subset of 20 PDFs across 2 categories included in this repo).

---

## Prerequisites

| Requirement | Version / Notes |
|---|---|
| Python | 3.11 or later |
| Embedding model | `text-embedding-3-small-1` via the EPAM DIAL proxy (no local install) |
| API key | EPAM DIAL proxy (Azure OpenAI compatible) — used for both chat completions and embeddings; see Configuration below |

Both the LLM and the embedding model are served by the EPAM DIAL proxy, so only the API key below is required before running ingestion.

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Configuration

The LLM is accessed through the EPAM DIAL proxy. Credentials are set in `src/config.py`:

```python
OPENAI_API_KEY  = "your-dial-api-key"
OPENAI_MODEL    = "gpt-4o"
AZURE_ENDPOINT  = "https://ai-proxy.lab.epam.com"
AZURE_API_VERSION = "2023-07-01-preview"
```

Replace `OPENAI_API_KEY` with your key, or export it as an environment variable and read it with `os.environ.get(...)`.

---

## Running the App

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`.

---

## Features

### Ingestion Tab

Point the app at the `data/` folder (default) and click **Start Ingestion**:

1. PDFs are extracted with **PyMuPDF**
2. Text is split into 512-token chunks with a 50-token overlap (**LlamaIndex SentenceSplitter**)
3. Chunks are embedded via the **EPAM DIAL / Azure OpenAI proxy** (`text-embedding-3-small-1`) and stored in **ChromaDB**
4. Structured fields (skills, years of experience, education, job titles) are extracted via the LLM and stored in **TinyDB**

**Incremental updates**: Re-running ingestion skips unchanged files (SHA-256 hash comparison), re-ingests modified files in-place, and removes deleted files from both stores — no full rebuild needed.

### Search & Ask Tab

Type any natural-language question (e.g. *"Which candidates have cloud infrastructure experience?"*) and click **Search & Ask**:

1. The question is embedded and used to retrieve the top-K most relevant resume chunks from ChromaDB
2. Retrieved chunks are passed as context to the LLM, which streams an answer
3. Source resume IDs and the raw chunks are displayed below the answer for transparency

### Analytics Tab

Interactive charts derived from the structured TinyDB data:

| Chart | Description |
|---|---|
| **Top Skills** | Horizontal bar chart of skill frequency across all resumes |
| **Seniority Distribution** | Donut pie chart (Junior 0–2 yrs · Mid 3–6 yrs · Senior 7+) |
| **Years of Experience** | Histogram of experience distribution |

Charts update when filtered by category (Engineering / IT).

### Access Control (Sidebar)

Select a role before searching or browsing analytics:

| Role | Scope | PII |
|---|---|---|
| **HR** | All categories | Visible |
| **Hiring Manager** | Engineering + IT only | Visible |
| **Recruiter** | All categories | Redacted (email, phone, address) |

The active role is applied to retrieval filters and LLM prompt context.

---

## Evaluation

RAG quality is measured with [RAGAS](https://docs.ragas.io/) across 5 question–answer pairs from `evaluation/golden_dataset.json`.

### Results (`evaluation/results_ragas.json`)

| Metric | Score |
|---|---|
| Faithfulness | **0.900** |
| Answer Relevancy | **0.603** |
| Context Precision | **0.683** |
| Context Recall | **0.800** |

**Faithfulness** measures whether the generated answer is grounded in the retrieved context (no hallucination). A score of 0.90 means 90 % of answer claims are directly supported by the retrieved chunks.

### Re-running Evaluation

```bash
python evaluation/evaluate_ragas_v2.py
```

Results are written to `evaluation/results_ragas.json`. The golden dataset can be edited at `evaluation/golden_dataset.json` to add or modify Q&A pairs.

---

## Assignment Coverage

| Requirement | How it is met |
|---|---|
| **GenAI framework** | LlamaIndex for chunking + embedding pipeline; RAGAS for evaluation |
| **Document analysis** | PDF resumes parsed with PyMuPDF; structured fields extracted by LLM |
| **Data visualization** | Plotly charts: skill frequency bar, seniority pie, experience histogram (Analytics tab) |
| **Evaluation metric** | RAGAS: faithfulness, answer relevancy, context precision, context recall — all evaluated on a 5-sample golden dataset |
| ⭐ **Ninja: Corpus update w/o Vector DB rebuild** | SHA-256 hash diffing in `src/ingestion/pipeline.py`; only changed/deleted resumes are updated |
| ⭐ **Ninja: Access control aware RAG** | Role selector in sidebar; `allowed_categories` filter passed to ChromaDB; PII redaction applied to Recruiter role |
| ⭐ **Ninja: Evaluate RAG** | RAGAS evaluation script with precision, recall, faithfulness, and answer relevancy metrics |

---

## Project Structure

```
app.py                        # Streamlit UI
src/
  config.py                   # Paths, model names, API credentials
  ingestion/
    extractor.py              # PDF text extraction
    chunker.py                # Chunk, embed, store in ChromaDB
    structured.py             # LLM-based structured field extraction → TinyDB
    pipeline.py               # Ingestion orchestration with hash-based diffing
  search/
    retriever.py              # Vector similarity search
    qa.py                     # Streaming LLM Q&A
  analytics/
    aggregator.py             # TinyDB queries for charts
  access/
    policy.py                 # Role definitions and PII redaction
data/                         # PDF resume corpus
db/
  chroma/                     # ChromaDB vector store
  resumes.json                # TinyDB structured metadata
evaluation/
  golden_dataset.json         # 5-sample Q&A evaluation set
  evaluate_ragas_v2.py        # RAGAS evaluation script
  results_ragas.json          # Latest evaluation results
requirements.txt
```
