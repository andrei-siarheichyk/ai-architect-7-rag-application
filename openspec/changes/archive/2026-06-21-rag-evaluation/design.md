## Context

The Resume Analyzer is a RAG system that embeds resume chunks and answers user questions using retrieval-augmented generation. Currently, there is no quantitative assessment of whether:
1. The retriever finds relevant resumes
2. The LLM answers faithfully (doesn't hallucinate)
3. The LLM answers address the user's question

RAGAS (Retrieval-Augmented Generation Assessment) is a framework designed specifically for RAG evaluation. It provides LLM-based metrics that don't require manual annotation at scale, making it practical for iterative improvement.

## Goals / Non-Goals

**Goals:**
- Build a test dataset that represents realistic user queries and covers diverse question types
- Integrate RAGAS evaluation to measure faithfulness, relevance, and context precision
- Create a repeatable evaluation workflow that shows system quality on the test set
- Enable rapid iteration and quality improvements via metric feedback

**Non-Goals:**
- Evaluate role-based access control (handled separately)
- Build a large-scale evaluation set (30-40 questions is sufficient for baseline)
- Achieve perfect metric scores (goal is to establish baseline and identify gaps)
- Replace manual human review (automated metrics complement but don't eliminate human judgment)

## Decisions

### Decision: Auto-generate questions, then user review
We will programmatically generate 40-50 questions from randomly sampled resumes, then ask the user to filter/edit for quality.

**Rationale**: Fully manual creation (selecting resumes, writing questions) would be time-consuming. Auto-generation gets us 80% of the way there quickly, and user review ensures quality without being burdensome.

**Alternative considered**: Fully manual creation—more curated but much slower. User confirmed light editing is acceptable.

### Decision: Use actual retriever output for contexts
Each test case's `contexts` field will contain real text chunks returned by the retriever for that question.

**Rationale**: RAGAS evaluates faithfulness against provided context. Using actual retriever output makes the evaluation realistic—it tests what the system *actually does*, not hypothetical perfect context. If retrieval is poor, that surfaces in the metrics.

**Alternative considered**: Manually write ideal context snippets—cleaner but doesn't measure retrieval quality.

### Decision: Structure test dataset in RAGAS format
Test dataset will be saved as JSON with fields: `question`, `answer`, `contexts` (list), `ground_truth`.

**Rationale**: RAGAS expects this exact structure. This format is also human-readable for review.

### Decision: Use Azure OpenAI for RAGAS metric scoring
RAGAS metrics (faithfulness, relevance, semantic similarity) are LLM-based. We'll use the existing Azure OpenAI setup via the RAGAS integration.

**Rationale**: We already have Azure OpenAI configured. RAGAS has built-in support for it. No new infrastructure needed.

**Alternative considered**: Use a local LLM via Ollama—would avoid API costs but metrics require strong reasoning (Claude/GPT perform better).

### Decision: Extract ground truth from sampled resume data
For each question, `ground_truth` will be manually extracted from the sampled resumes (e.g., if the question is "What languages does Alice know?", the answer is extracted from her resume).

**Rationale**: Provides a target for semantic similarity metrics. Also allows us to verify that RAGAS faithfulness scores align with reality.

### Decision: Store evaluation results separately
Results will be saved to `evaluation/results.json` after each run, not embedded in the dataset.

**Rationale**: Allows the test dataset to remain static while results can be recomputed. Easier to compare across runs.

## Risks / Trade-offs

**[Risk] Auto-generated questions may not match real user patterns**
→ *Mitigation*: User reviews and filters questions before evaluation runs. Can expand with real user queries later.

**[Risk] Small dataset (30-40 questions) may not catch all issues**
→ *Mitigation*: This is a baseline. Metrics will guide expansion. If scores are good on this set but users report issues, we expand the test set.

**[Risk] RAGAS metrics rely on LLM judgement, which can be inconsistent**
→ *Mitigation*: Use consistent model/temperature settings. Run evaluation multiple times to check variance. Consider this exploratory first pass.

**[Risk] Azure OpenAI calls for evaluation will incur costs**
→ *Mitigation*: Small dataset (~40 questions × 3-4 metrics) keeps costs low. Evaluation is infrequent (not on every commit).

## Migration Plan

**Phase 1**: Generate test dataset + get user review
- Sample 10-12 resumes
- Auto-generate ~40-50 questions
- User reviews, filters to final set (~30-40)
- Extract ground truth

**Phase 2**: Implement RAGAS evaluation script
- Install RAGAS library
- Build evaluation runner that executes full pipeline per question
- Integrate with Azure OpenAI for metric scoring
- Generate results and summary report

**Phase 3**: Run baseline evaluation
- Execute full test set
- Document baseline metrics
- Identify any notably weak areas

No rollback needed—purely additive feature.

## Open Questions

1. Should evaluation run automatically in CI, or manually on-demand? (Plan: manual for now, CI integration later)
2. What metric thresholds define "acceptable" performance? (Plan: establish baseline first, then set targets)
3. Should we store per-question results for debugging, or just aggregate metrics? (Plan: store both)
