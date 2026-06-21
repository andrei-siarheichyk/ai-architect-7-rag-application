## Context

The Search tab in `app.py` (lines 87–135) has two independent interaction phases:

1. A `st.text_input("Search query")` + `st.button("Search")` that runs vector retrieval and stores results in `st.session_state["search_results"]`.
2. A second `st.text_input("Question")` + `st.button("Ask")` that appears only after results exist and streams an LLM answer.

Users must articulate the same intent twice. The backend (`search()` + `answer_stream()`) already accepts a single question string for both retrieval and Q&A, so the two-step UI is purely an artifact of how the tab was initially built.

## Goals / Non-Goals

**Goals:**
- One text input field for the user's question
- One "Search & Ask" button that calls `search()` then immediately calls `answer_stream()` in sequence
- Display streamed LLM answer first, then expand the retrieved chunks beneath it
- Preserve the `top_k` slider and role-based access control behaviour

**Non-Goals:**
- Changing any backend module (`retriever.py`, `qa.py`, etc.)
- Adding result caching or pagination
- Changing the Ingestion or Analytics tabs

## Decisions

**Single session-state key retained** — `st.session_state["search_results"]` is still written after retrieval so the chunk expanders can render on Streamlit re-runs without re-querying. The answer text is not persisted to session state (it streams live on each button click, consistent with how `st.write_stream` works).

**Answer displayed before chunks** — The LLM answer is the primary user output; the retrieved chunks are supporting evidence. Displaying answer first then chunks matches this priority without needing a layout change like columns.

**No intermediate spinner split** — A single `st.spinner("Searching & answering…")` wraps both `search()` and the start of `answer_stream()`; streaming begins as soon as the first token arrives.

## Risks / Trade-offs

- **Re-run behaviour**: Streamlit re-runs the whole script on any widget interaction. The streamed answer is not stored, so switching tabs and returning clears the answer (chunks remain via session state). This is acceptable and consistent with current behaviour.
- **Latency perception**: Combining retrieval + generation means the button appears to "think" longer before output appears. Mitigated by streaming — first tokens appear as soon as generation starts.

## Migration Plan

Pure in-place edit of the Search tab block in `app.py`. No data migration, no config changes. Rollback is reverting the file edit.
