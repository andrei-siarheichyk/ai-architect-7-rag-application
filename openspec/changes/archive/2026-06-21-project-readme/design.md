## Context

The project is a working Streamlit application. No code changes are needed; the only deliverable is `README.md` at the project root.

## Goals / Non-Goals

**Goals:**
- Single `README.md` that lets a new developer clone, install, and run the app without reading source code
- Clearly maps each assignment requirement to the feature that satisfies it
- Includes actual RAGAS scores from `evaluation/results_ragas.json`

**Non-Goals:**
- API reference or architecture deep-dive
- Changes to any source file

## Decisions

**Single flat README, no sub-docs** — The project is small enough that one file covers everything without becoming unwieldy.

**Ordered setup sections** — Prerequisites → Install → Configure → Run matches the mental model of a developer starting from scratch.

**Assignment coverage table** — A concise table mapping each requirement / Ninja challenge to the relevant feature makes grading straightforward.

## Risks / Trade-offs

- EPAM DIAL API key in `src/config.py` is hardcoded; README should note this and suggest setting it via environment variable or config edit before running.
- Ollama must be running locally; README must call this out as a prerequisite with the model pull command.
