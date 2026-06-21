## Why

The Resume Analyzer RAG system generates answers by retrieving resume chunks and using an LLM to synthesize responses. Currently, there is no quantitative measurement of output quality—we don't know if answers are faithful to the retrieved context, whether the retriever finds relevant resumes, or how well the system answers questions. This must be evaluated before expanding to production users.

## What Changes

We will implement a RAGAS-based evaluation framework that:
- Creates a test dataset of 30-40 diverse Q&A pairs sampled from real resumes
- Runs the full system (retrieval + generation) on each test question
- Scores outputs on multiple metrics: faithfulness, answer relevance, context precision, semantic similarity
- Provides a baseline for tracking quality improvements

## Capabilities

### New Capabilities

- `generative-model-evaluation`: Framework for measuring RAG output quality using RAGAS. Includes test dataset creation, evaluation script, and metric reporting.

### Modified Capabilities

(None)

## Impact

- **New dependencies**: RAGAS library for LLM-based evaluation metrics
- **New code**: `evaluation/` directory with dataset, evaluation script, results
- **Affected systems**: Uses existing retriever and QA generation; relies on Azure OpenAI for metric scoring
- **No breaking changes**: Pure addition, no existing functionality modified
