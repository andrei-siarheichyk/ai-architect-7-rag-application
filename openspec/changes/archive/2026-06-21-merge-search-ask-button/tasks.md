## 1. Rewrite Search Tab in app.py

- [x] 1.1 Replace `st.text_input("Search query", ...)` with `st.text_input("Question", ...)` and update placeholder to reflect the combined intent
- [x] 1.2 Remove the `st.button("Search")` block and its inner logic
- [x] 1.3 Remove the `if results:` block containing the separate "Question" input and `st.button("Ask")`
- [x] 1.4 Add a single `st.button("Search & Ask", type="primary")` that, when clicked with a non-empty query, calls `search()` storing results in `st.session_state["search_results"]`, then immediately streams `answer_stream()` and shows source IDs caption
- [x] 1.5 After the button block, render `st.session_state.get("search_results", [])` as expandable chunk items (the existing expander loop, moved below the answer)

## 2. Verify Correctness

- [x] 2.1 Confirm empty input shows a warning and does not call backend
- [x] 2.2 Confirm a valid question shows the streamed answer followed by the chunk expanders and source caption
- [x] 2.3 Confirm role-scoped filtering and PII redaction still apply (switch role in sidebar and re-run)
