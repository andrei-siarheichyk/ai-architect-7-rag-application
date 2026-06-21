## Why

The Search tab currently requires two separate interactions — a "Search" button to retrieve resume chunks and an "Ask" button to answer a question about them — forcing the user to fill in two inputs and click twice for what is a single intent: ask a question and get an answer. Merging them into one action removes the friction and makes the flow match how users naturally think about the feature.

## What Changes

- Remove the separate "Search" and "Ask" buttons from the Search tab
- Introduce a single input field that accepts the user's question (replacing the current split between "Search query" and "Question")
- Introduce a single "Search & Ask" button that triggers retrieval followed immediately by streaming Q&A
- Retrieved chunks are still displayed below the answer so the user can inspect sources
- The `search_results` session-state key is retained so the results panel renders correctly on re-runs

## Capabilities

### New Capabilities

- `unified-search-ask`: Single-action flow that runs vector retrieval and LLM Q&A in sequence from one input and one button click; renders the streamed answer first, then the supporting resume chunks

### Modified Capabilities

(none — no existing specs to delta)

## Impact

- `app.py`: Search tab section rewritten; two `st.button` calls and two `st.text_input` calls collapsed into one of each
- No changes to `src/search/retriever.py`, `src/search/qa.py`, or any backend module
- No new dependencies
