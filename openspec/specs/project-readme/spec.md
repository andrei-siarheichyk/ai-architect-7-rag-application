## Purpose

The project README documents setup, configuration, usage, evaluation, and assignment coverage so a developer can run the app from a clean clone.
## Requirements
### Requirement: README exists at project root
The repository SHALL contain a `README.md` at the root level that covers setup, usage, and assignment coverage.

#### Scenario: File present
- **WHEN** a developer clones the repository
- **THEN** `README.md` SHALL be present at the root and readable without any build step

### Requirement: Prerequisites section
The README SHALL list all prerequisites a developer needs before running the app: Python version and the EPAM DIAL / Azure OpenAI API key (used for both chat completions and embeddings). The README SHALL NOT require a local Ollama installation or model pull.

#### Scenario: Embedding model called out
- **WHEN** a developer reads the Prerequisites section
- **THEN** the DIAL / Azure OpenAI embedding model `text-embedding-3-small-1` and the required API key SHALL be documented so embeddings work before ingestion, with no `ollama pull` step

### Requirement: Installation and run instructions
The README SHALL provide copy-pasteable commands to install dependencies and start the Streamlit app.

#### Scenario: Install and launch
- **WHEN** a developer follows the Installation section
- **THEN** running `pip install -r requirements.txt` followed by `streamlit run app.py` SHALL start the application

### Requirement: Feature descriptions
The README SHALL describe the three main tabs — Ingestion, Search & Ask, and Analytics — and the role-based access control sidebar.

#### Scenario: Ingestion described
- **WHEN** a developer reads the Features section
- **THEN** they SHALL understand that PDF resumes are chunked, embedded via the EPAM DIAL / Azure OpenAI proxy, and stored in ChromaDB

#### Scenario: Search & Ask described
- **WHEN** a developer reads the Features section
- **THEN** they SHALL understand that a single question field triggers vector retrieval followed by streaming LLM Q&A

### Requirement: Evaluation section with RAGAS scores
The README SHALL include a table of RAGAS evaluation metrics from `evaluation/results_ragas.json` and instructions for re-running the evaluation script.

#### Scenario: Metrics visible
- **WHEN** a developer reads the Evaluation section
- **THEN** they SHALL see faithfulness, answer relevancy, context precision, and context recall scores alongside the command to reproduce them

### Requirement: Assignment coverage summary
The README SHALL contain a section that maps each assignment requirement and Ninja challenge to the feature or file that satisfies it.

#### Scenario: All requirements listed
- **WHEN** a developer reads the Assignment Coverage section
- **THEN** every base requirement and every completed Ninja challenge SHALL appear with a one-line description of how it is implemented

