## 1. Setup

- [x] 1.1 Add `plotly` to `requirements.txt` and install it
- [x] 1.2 Create `src/analytics/__init__.py` and `src/analytics/aggregator.py`

## 2. Aggregator

- [x] 2.1 Implement `get_categories() -> list[str]` — return sorted list of unique categories from TinyDB
- [x] 2.2 Implement `skill_frequency(category: str | None, top_n: int) -> list[tuple[str, int]]` — count skill occurrences across TinyDB docs (optionally filtered by category), return top-N sorted by count descending
- [x] 2.3 Implement `seniority_distribution(category: str | None) -> dict[str, int]` — bucket resumes into Junior (0–2), Mid (3–6), Senior (7+) by `years_exp`, return `{"Junior": n, "Mid": n, "Senior": n}`
- [x] 2.4 Implement `experience_values(category: str | None) -> list[int]` — return raw `years_exp` values for histogram rendering

## 3. Analytics Tab

- [x] 3.1 Add "Analytics" to `st.tabs` in `app.py` (alongside Ingestion and Search)
- [x] 3.2 Add empty-store guard: if TinyDB has no documents, show warning "No resumes ingested yet"
- [x] 3.3 Add category dropdown (All + each category from `get_categories()`) and top-N slider (5–50, default 20)
- [x] 3.4 Render skill frequency horizontal bar chart with `st.plotly_chart` using `plotly.graph_objects.Bar`
- [x] 3.5 Render seniority pie chart with `plotly.graph_objects.Pie`
- [x] 3.6 Render experience histogram with `plotly.graph_objects.Histogram`
