## Context

The app has three tabs (Ingestion, Search, Analytics) with no access differentiation. Retrieval goes through `src/search/retriever.py` (ChromaDB query), generation through `src/search/qa.py` (AzureOpenAI), and analytics through `src/analytics/aggregator.py` (TinyDB). All three need to respect the active role.

## Goals / Non-Goals

**Goals:**
- Single `POLICIES` dict as the authoritative source of access rules — no role logic scattered across modules
- Retrieval filter: pass `where` clause to ChromaDB only when a category allowlist applies
- Generation redaction: regex scrub of chunk text before prompt assembly for roles with `redact_pii: True`
- Analytics scoping: pass `allowed_categories` to all aggregator functions
- Demo-grade auth: sidebar dropdown, role stored in `st.session_state["role"]`

**Non-Goals:**
- Real authentication (passwords, tokens, sessions)
- Row-level security beyond category filtering
- Guaranteed PII removal (regex is best-effort; stated as a known limitation)
- Audit logging of access

## Decisions

**Policy as a plain dict in `src/access/policy.py`**
A single `POLICIES` dict is readable, testable, and trivially extended. Alternatives (YAML config, DB table) add indirection with no benefit at this scale.

**Retrieval filter via ChromaDB `where` clause, not post-filter**
Filtering after retrieval would mean wrong-category chunks silently consume the top-K budget. Pushing the filter into the query ensures the result set only contains permitted documents. ChromaDB supports `where={"category": {"$in": [...]}}` natively.

**Redaction before prompt assembly, not after LLM response**
Scrubbing the LLM's output is unreliable — the model may paraphrase PII. Scrubbing the *input* context means the model never sees it and cannot reproduce it. Trade-off: regex false negatives still possible (unusual phone formats, international addresses).

**Role selector in sidebar, not a login page**
Demo context. A `st.sidebar.selectbox` sets `st.session_state["role"]` on every interaction. No persistence across browser sessions — intentional for a demo.

## Module layout

```
src/
└── access/
    ├── __init__.py
    └── policy.py       # POLICIES dict + get_policy(role) + redact(text, role)
```

## Policy structure

```python
POLICIES = {
    "HR": {
        "allowed_categories": None,   # None = no filter applied
        "redact_pii": False,
    },
    "Hiring Manager": {
        "allowed_categories": ["Engineering", "Information-Technology"],
        "redact_pii": False,
    },
    "Recruiter": {
        "allowed_categories": None,
        "redact_pii": True,
    },
}
```

## Integration points

```
sidebar role selector
        │
        ▼ st.session_state["role"]
        │
        ├──► retriever.search(query, top_k, allowed_categories=policy["allowed_categories"])
        │         └── ChromaDB where={"category": {"$in": allowed}} if allowed else no filter
        │
        ├──► qa.answer_stream(question, results, redact_pii=policy["redact_pii"])
        │         └── redact(chunk_text, role) applied to each chunk before prompt
        │
        └──► aggregator.*( category_filter, allowed_categories=policy["allowed_categories"])
                  └── TinyDB search scoped to allowed categories if set
```

## Risks / Trade-offs

- **Regex PII miss rate** → documented as best-effort; not a security guarantee
- **Session state reset on page refresh** → user must re-select role; acceptable for demo
- **Hiring Manager category list is hardcoded** → Engineering + IT; real system would load from user profile
