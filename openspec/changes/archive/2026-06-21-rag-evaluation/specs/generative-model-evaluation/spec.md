## ADDED Requirements

### Requirement: Test dataset for RAG evaluation
The system SHALL define a test dataset in RAGAS format containing 30-40 question-answer-context tuples sourced from randomly sampled resumes, suitable for comprehensive evaluation of retrieval and generation quality.

#### Scenario: Dataset is created from diverse question types
- **WHEN** the dataset is generated
- **THEN** it includes skill-based queries (e.g., "Who knows Python?"), role-based queries (e.g., "Find product managers"), experience-based queries (e.g., "Who has 5+ years of leadership?"), and comparative queries (e.g., "Compare Alice vs Bob's experience")

#### Scenario: Contexts are actual retrieved chunks
- **WHEN** the dataset is generated
- **THEN** each test case's `contexts` field contains real text chunks from the retriever (not summaries), allowing RAGAS to evaluate against actual system outputs

#### Scenario: Ground truth is extracted from sampled resumes
- **WHEN** the dataset is generated
- **THEN** `ground_truth` field for each question is manually extracted from the sampled resume data to serve as the evaluation target

### Requirement: RAGAS evaluation execution
The system SHALL execute RAGAS evaluation metrics on the test dataset, scoring each Q&A pair on multiple dimensions of quality and returning structured results.

#### Scenario: System runs full pipeline for each test question
- **WHEN** evaluation is triggered
- **THEN** for each test question, the system runs: retrieve relevant resumes → generate LLM answer → evaluate with RAGAS

#### Scenario: Faithfulness metric is computed
- **WHEN** evaluation runs
- **THEN** each answer is scored on faithfulness (whether the answer is grounded in the provided context, using LLM-based evaluation)

#### Scenario: Answer relevance metric is computed
- **WHEN** evaluation runs
- **THEN** each answer is scored on relevance (whether the answer actually addresses the question, using LLM-based evaluation)

#### Scenario: Context precision metric is computed
- **WHEN** evaluation runs
- **THEN** each retrieved context is scored on precision (whether the chunk is relevant to the question, using LLM-based evaluation)

### Requirement: Evaluation results are reported
The system SHALL produce a structured evaluation report showing metrics across the test dataset, enabling assessment of overall system quality and identification of weak areas.

#### Scenario: Results are saved in machine-readable format
- **WHEN** evaluation completes
- **THEN** results are saved to `evaluation/results.json` with per-question scores and aggregate statistics

#### Scenario: Report summarizes aggregate metrics
- **WHEN** results are generated
- **THEN** summary statistics are computed for each metric (mean, min, max, std dev) across all test questions

#### Scenario: Report is human-readable
- **WHEN** evaluation completes
- **THEN** a summary report is generated showing overall quality assessment and any test questions with notably low scores

### Requirement: Evaluation dataset is user-reviewable
The system SHALL make the generated test dataset available for human review and lightweight editing before evaluation runs, allowing filtering of unsuitable questions.

#### Scenario: Dataset is formatted for review
- **WHEN** dataset is generated
- **THEN** it is saved in a readable format (JSON with clear structure) that a human can quickly review and manually edit

#### Scenario: User can filter questions
- **WHEN** reviewing the dataset
- **THEN** the user can delete or modify individual questions that don't feel natural or representative before running evaluation
