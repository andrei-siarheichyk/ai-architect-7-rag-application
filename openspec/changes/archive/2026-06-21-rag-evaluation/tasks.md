## 1. Setup and Dependencies

- [x] 1.1 Add RAGAS library to requirements.txt
- [x] 1.2 Create `evaluation/` directory structure
- [x] 1.3 Verify Azure OpenAI connection works for evaluation

## 2. Dataset Generation: Resume Sampling and Question Creation

- [x] 2.1 Write script to randomly sample 10-12 resumes from data dirs (one per category)
- [x] 2.2 Extract structured info from sampled resumes (skills, title, experience, projects)
- [x] 2.3 Auto-generate 40-50 diverse questions (skill-based, role-based, experience-based, comparative)
- [x] 2.4 For each question, run retriever to get actual context chunks
- [x] 2.5 Extract ground truth answers from sampled resume data
- [x] 2.6 Package as RAGAS-format JSON and save to `evaluation/test_dataset_raw.json`

## 3. Dataset Review and Finalization

- [x] 3.1 Generate human-readable preview of test questions for review
- [x] 3.2 User reviews `evaluation/test_dataset_raw.json`, deletes/edits unsuitable questions
- [x] 3.3 Save finalized dataset to `evaluation/test_dataset.json`

## 4. RAGAS Evaluator Implementation

- [x] 4.1 Create `evaluation/evaluate.py` script that loads test dataset
- [x] 4.2 Implement pipeline: for each test question, run full system (retrieve → generate answer)
- [x] 4.3 Integrate RAGAS metrics (faithfulness, answer relevance, context precision)
- [x] 4.4 Compute semantic similarity between LLM answer and ground truth
- [x] 4.5 Aggregate per-question results and compute summary statistics
- [x] 4.6 Save detailed results to `evaluation/results.json`

## 5. Reporting

- [x] 5.1 Generate human-readable summary report showing metric means, ranges, and any low-scoring questions
- [x] 5.2 Save summary to `evaluation/evaluation_report.md`

## 6. Documentation

- [x] 6.1 Create `evaluation/README.md` explaining test dataset structure
- [x] 6.2 Document how to run evaluation (`python evaluation/evaluate.py`)
- [x] 6.3 Document how to interpret metrics (what do faithfulness, relevance, etc. mean?)
- [x] 6.4 Document how to add new test cases to the dataset

## 7. Baseline Execution and Verification

- [x] 7.1 Run full evaluation pipeline end-to-end
- [x] 7.2 Verify results are sensible (no NaN/errors, scores in expected ranges)
- [x] 7.3 Document baseline metrics as reference for future improvements
