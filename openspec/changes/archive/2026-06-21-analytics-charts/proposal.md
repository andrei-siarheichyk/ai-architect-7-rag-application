## Why

TinyDB holds structured resume fields (skills, years_exp, education, job_titles) for every ingested resume, but there is no way to explore aggregate patterns across the corpus. An Analytics tab will turn this structured data into actionable charts: which skills dominate, how seniority distributes, and how experience spreads.

## What Changes

- Add an **Analytics** tab to the Streamlit app alongside Ingestion and Search
- Implement `src/analytics/aggregator.py` — query TinyDB and compute aggregations (skill frequency, seniority buckets, years-of-experience distribution)
- Render three charts with Plotly:
  - **Skill frequency** — horizontal bar chart of top-N skills across all (or filtered) resumes
  - **Seniority distribution** — pie chart bucketing resumes into Junior / Mid / Senior by `years_exp`
  - **Experience histogram** — histogram of `years_exp` values across the corpus
- Optional category filter — scope all charts to a selected category

## Capabilities

### New Capabilities
- `skill-frequency-chart`: aggregate skill counts from TinyDB, render top-N horizontal bar chart, filterable by category
- `seniority-distribution-chart`: bucket resumes by years_exp (Junior 0–2, Mid 3–6, Senior 7+), render pie chart
- `experience-histogram`: plot distribution of years_exp values as a histogram

### Modified Capabilities
- *(none)*

## Impact

- `app.py` — add Analytics tab
- New `src/analytics/` module — aggregation logic
- New dependency: `plotly` (chart rendering in Streamlit via `st.plotly_chart`)
- Reads from: TinyDB at `db/resumes.json`
