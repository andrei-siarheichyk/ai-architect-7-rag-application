## Why

The app currently gives every user identical access to all resume data. Adding role-based access control enforces who can retrieve which resumes and what sensitive fields the LLM is allowed to reveal — making the app suitable for a realistic HR demo with differentiated personas.

## What Changes

- Add a **role selector** to the Streamlit sidebar (HR / Hiring Manager / Recruiter) — no real auth, demo-mode
- Add `src/access/policy.py` — single source of truth for per-role access rules
- Enforce **retrieval-layer filtering**: Hiring Manager sees only Engineering + IT resumes (ChromaDB `where` filter)
- Enforce **generation-layer redaction**: Recruiter role strips PII (email, phone, address) from chunk text before it reaches the LLM prompt
- Scope **Analytics tab** charts to role-allowed categories

## Capabilities

### New Capabilities
- `role-selector`: Streamlit sidebar widget that sets the active role in session state; persists across tab switches
- `retrieval-access-control`: Per-role category allowlist applied as ChromaDB metadata filter at query time
- `generation-redaction`: Pre-LLM PII scrubbing for the Recruiter role; regex-based, applied to chunk text before prompt assembly

### Modified Capabilities
- *(none — new policy layer wraps existing retriever and QA without changing their interfaces)*

## Impact

- `app.py` — add sidebar role selector; pass role into search and analytics calls
- New `src/access/` module — `policy.py` with `POLICIES` dict and helper functions
- `src/search/retriever.py` — accept optional `allowed_categories` filter
- `src/search/qa.py` — accept `redact_pii` flag, apply redaction before building prompt
- `src/analytics/aggregator.py` — accept optional `allowed_categories` filter on all aggregation functions

## Access matrix

| Role | Categories | PII Redaction | Analytics scope |
|------|-----------|---------------|-----------------|
| HR | ALL | None | All categories |
| Hiring Manager | Engineering, Information-Technology | None | Engineering + IT only |
| Recruiter | ALL | Email, phone, address | All categories |
