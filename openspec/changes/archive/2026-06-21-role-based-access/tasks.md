## 1. Access Policy Module

- [x] 1.1 Create `src/access/__init__.py` and `src/access/policy.py` with `POLICIES` dict (HR / Hiring Manager / Recruiter), `get_policy(role) -> dict`, and `redact(text: str, role: str) -> str` (regex strips email, phone, address for `redact_pii: True` roles)

## 2. Retrieval Layer

- [x] 2.1 Update `src/search/retriever.py`: add `allowed_categories: list[str] | None = None` param to `search()`; pass `where={"category": {"$in": allowed_categories}}` to ChromaDB query when not None
- [x] 2.2 Update `src/analytics/aggregator.py`: add `allowed_categories: list[str] | None = None` param to `_load()`, `get_categories()`, `skill_frequency()`, `seniority_distribution()`, and `experience_values()`; filter TinyDB results to allowed categories when not None

## 3. Generation Layer

- [x] 3.1 Update `src/search/qa.py`: add `redact_pii: bool = False` param to `answer_stream()`; apply `redact(chunk_text, role)` to each result's text before building the prompt context

## 4. Streamlit Integration

- [x] 4.1 Add role selector to `app.py` sidebar: `st.sidebar.selectbox` with options HR / Hiring Manager / Recruiter, default HR, stored in `st.session_state["role"]`; show active role label below selector
- [x] 4.2 Wire policy into Search tab: call `get_policy(role)`, pass `allowed_categories` to `search()`, pass `redact_pii` to displayed chunk text and to `answer_stream()`
- [x] 4.3 Wire policy into Analytics tab: pass `allowed_categories` from policy to all three aggregator calls; show active role and scope note in the tab header
