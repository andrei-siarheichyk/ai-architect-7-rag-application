import json
import sys
import types
from pathlib import Path

# Stub nest_asyncio BEFORE any RAGAS imports.
# RAGAS executor calls nest_asyncio.apply() at module load time (executor.py:15).
# In Python 3.14, nest_asyncio's asyncio patches break asyncio.current_task()
# inside created tasks, causing asyncio.timeout() to raise RuntimeError.
# A no-op stub keeps asyncio's task context tracking intact.
_fake_nest = types.ModuleType("nest_asyncio")
_fake_nest.apply = lambda: None
sys.modules["nest_asyncio"] = _fake_nest

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import OPENAI_API_KEY, AZURE_ENDPOINT, AZURE_API_VERSION, OPENAI_MODEL
from src.search.qa import answer_stream as qa_answer_stream

try:
    from ragas import evaluate
    from ragas.llms import LangchainLLMWrapper
    from ragas.embeddings import LangchainEmbeddingsWrapper
    from ragas.dataset_schema import SingleTurnSample, EvaluationDataset
    from ragas.metrics import Faithfulness, ResponseRelevancy, ContextPrecision, ContextRecall
except ImportError as e:
    print(f"Error: RAGAS not available: {e}")
    sys.exit(1)


def run_full_pipeline(question: str, contexts: list[str]) -> str:
    answer_text = ""
    try:
        def parse_ctx(ctx: str) -> dict:
            # context strings are formatted as "{resume_id} · {category} - {text}"
            if " · " in ctx and " - " in ctx:
                resume_id, rest = ctx.split(" · ", 1)
                category, text = rest.split(" - ", 1)
            else:
                resume_id, category, text = "unknown", "unknown", ctx
            return {"text": text, "resume_id": resume_id.strip(), "category": category.strip()}

        formatted = [parse_ctx(ctx) for ctx in contexts]
        for chunk in qa_answer_stream(question, formatted):
            answer_text += chunk
    except Exception as e:
        print(f"    Warning: generation failed: {e}")
        answer_text = f"Error: {str(e)[:100]}"
    return answer_text


def load_dataset(path: Path) -> EvaluationDataset:
    with open(path) as f:
        raw = json.load(f)
    print(f"Generating live responses for {len(raw)} test cases...")
    samples = []
    for i, item in enumerate(raw, 1):
        question = item["user_input"]
        print(f"  [{i}/{len(raw)}] {question[:65]}...")
        answer = run_full_pipeline(question, item["retrieved_contexts"])
        samples.append(
            SingleTurnSample(
                user_input=question,
                response=answer,
                retrieved_contexts=item["retrieved_contexts"],
                reference=item.get("reference", ""),
            )
        )
    return EvaluationDataset(samples=samples)


def setup_evaluator():
    try:
        from langchain_openai import AzureChatOpenAI
    except ImportError:
        print("Error: langchain-openai not installed. Run: pip install langchain-openai")
        sys.exit(1)

    llm = AzureChatOpenAI(
        azure_endpoint=AZURE_ENDPOINT,
        api_key=OPENAI_API_KEY,
        api_version=AZURE_API_VERSION,
        azure_deployment=OPENAI_MODEL,
        temperature=0,
    )

    # Use same Ollama embeddings the RAG system uses — EPAM DIAL has no embeddings deployment
    from src.config import EMBED_MODEL, OLLAMA_BASE_URL
    try:
        from langchain_ollama import OllamaEmbeddings
        embeddings = OllamaEmbeddings(model=EMBED_MODEL, base_url=OLLAMA_BASE_URL)
    except ImportError:
        from langchain_community.embeddings import OllamaEmbeddings
        embeddings = OllamaEmbeddings(model=EMBED_MODEL, base_url=OLLAMA_BASE_URL)

    return LangchainLLMWrapper(llm), LangchainEmbeddingsWrapper(embeddings)


if __name__ == "__main__":
    print("=" * 70)
    print("RAGAS Evaluation — Azure OpenAI via EPAM DIAL")
    print("=" * 70)

    dataset_path = Path(__file__).parent / "golden_dataset.json"
    if not dataset_path.exists():
        print(f"Error: dataset not found at {dataset_path}")
        sys.exit(1)

    dataset = load_dataset(dataset_path)

    print("\nSetting up RAGAS evaluator (Azure OpenAI)...")
    evaluator_llm, evaluator_embeddings = setup_evaluator()

    metrics = [
        Faithfulness(llm=evaluator_llm),
        ResponseRelevancy(llm=evaluator_llm, embeddings=evaluator_embeddings),
        ContextPrecision(llm=evaluator_llm),
        ContextRecall(llm=evaluator_llm),
    ]

    print("\nRunning RAGAS evaluation...")
    print("=" * 70)
    result = evaluate(dataset=dataset, metrics=metrics)

    out_dir = Path(__file__).parent
    #csv_path = out_dir / "results_ragas.csv"
    json_path = out_dir / "results_ragas.json"

    df = result.to_pandas()
    #df.to_csv(csv_path, index=False)
    with open(json_path, "w") as f:
        json.dump(df.to_dict(orient="records"), f, indent=2, default=str)

    print("\n" + "=" * 70)
    print("Evaluation Summary")
    print("=" * 70)
    scores = {
        col: round(float(df[col].mean()), 4)
        for col in ["faithfulness", "answer_relevancy", "context_precision", "context_recall"]
        if col in df.columns
    }
    for metric, score in scores.items():
        print(f"  {metric:<22} {score:.4f}")
    print("=" * 70)
    print(f"\nDetailed results saved to:")
    #print(f"  {csv_path}")
    print(f"  {json_path}")
