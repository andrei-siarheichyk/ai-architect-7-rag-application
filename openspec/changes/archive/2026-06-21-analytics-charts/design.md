## Context

TinyDB at `db/resumes.json` stores one document per resume with fields: `resume_id`, `category`, `skills` (list), `years_exp` (int), `education`, `job_titles`, `certifications`, `chunk_count`, `ingested_at`.

The Streamlit app has two tabs (Ingestion, Search). This change adds a third: Analytics.

## Goals / Non-Goals

**Goals:**
- Aggregate TinyDB data into frequency counts and distributions entirely in Python (no SQL, no external service)
- Render three Plotly charts in Streamlit: skill frequency bar, seniority pie, experience histogram
- Category dropdown to scope all three charts to a single job category

**Non-Goals:**
- Real-time updates as ingestion runs (charts load on tab open)
- Export charts as images
- Cross-field correlations (e.g. skills by education level)

## Decisions

**Plotly over Matplotlib**
Streamlit renders Plotly charts interactively (hover, zoom) via `st.plotly_chart`. Matplotlib produces static images — worse UX for no benefit here.

**Aggregation in Python (not a DB query)**
TinyDB has no aggregation API. Loading all documents and computing counts in Python with `collections.Counter` is simpler and fast enough for 2400 records. Alternative (DuckDB over the JSON file) would be over-engineered for this scale.

**Seniority buckets: Junior 0–2, Mid 3–6, Senior 7+**
Common industry convention. Hard-coded thresholds are good enough; no config needed for a demo.

**Module layout**
```
src/
└── analytics/
    ├── __init__.py
    └── aggregator.py   # all aggregation logic; returns plain dicts/lists for Plotly
```

Charts are built directly in `app.py` using `plotly.graph_objects` — keeps the aggregator testable and chart-agnostic.

## Risks / Trade-offs

- **Empty TinyDB** → all aggregations return empty collections. UI must detect this and show a prompt to run ingestion first. Same guard pattern as Search tab.
- **Resumes with `years_exp = 0`** → ambiguous (unknown vs. truly 0 years). Included in Junior bucket; acceptable for a demo.
- **Skills list quality depends on LLM extraction** — noisy or missing skills will skew the frequency chart. Nothing to mitigate here; it's a data quality issue upstream.
