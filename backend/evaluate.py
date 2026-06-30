"""
eval_retrieval.py

Evaluates whether the RAG pipeline retrieves the CORRECT chunks for a given
question, and whether the final answer is faithful/relevant.

Two layers of evaluation:
  1. Manual IR metrics (Precision@k, Recall@k, Hit Rate, MRR) against a
     hand-labeled test set you define yourself (ground truth keywords/IDs).
  2. RAGAS metrics (context_precision, context_recall, faithfulness,
     answer_relevancy) using your local Ollama model as the judge — so the
     whole evaluation stays offline, matching the rest of the project.

Run:
    pip install ragas datasets langchain-ollama --break-system-packages
    python eval_retrieval.py
"""

from pathlib import Path

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

BASE_DIR = Path(__file__).resolve().parent
VECTOR_DB_DIR = BASE_DIR / "vectordb"

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = Chroma(persist_directory=str(VECTOR_DB_DIR), embedding_function=embeddings)

# ---------------------------------------------------------------------------
# 1. LABELED TEST SET
# ---------------------------------------------------------------------------
# For each question, list keywords/phrases that MUST appear in a chunk for
# that chunk to count as "relevant". This avoids needing exact chunk IDs,
# which change every time you re-ingest.
#
# Tip: pick keywords that are specific enough to not appear in unrelated
# chunks (e.g. a disease name, a unique term), not generic words.
TEST_SET = [
    {
        "question": "What are the symptoms of anemia?",
        "relevant_keywords": ["anemia", "fatigue", "pale"],
    },
    {
        "question": "What causes asthma attacks?",
        "relevant_keywords": ["asthma", "bronchi", "airway"],
    },
    {
        "question": "What is an abscess and how does it form?",
        "relevant_keywords": ["abscess", "pus", "infection"],
    },
    {
        "question": "What are the common treatments for acne?",
        "relevant_keywords": ["acne", "sebaceous", "pimples"],
    },
    {
        "question": "How is AIDS transmitted?",
        "relevant_keywords": ["AIDS", "HIV", "immune"],
    },
    {
        "question": "What are the effects of chronic alcoholism on the body?",
        "relevant_keywords": ["alcoholism", "liver", "dependence"],
    },
    {
        "question": "What triggers an allergic reaction?",
        "relevant_keywords": ["allergy", "antigen", "histamine"],
    },
    {
        "question": "What are the early signs of Alzheimer's disease?",
        "relevant_keywords": ["alzheimer", "memory", "dementia"],
    },
    {
        "question": "What is an aneurysm and why is it dangerous?",
        "relevant_keywords": ["aneurysm", "artery", "rupture"],
    },
    {
        "question": "What causes angina pain?",
        "relevant_keywords": ["angina", "chest pain", "heart"],
    },
    {
        "question": "What are the symptoms of anorexia nervosa?",
        "relevant_keywords": ["anorexia", "eating disorder", "weight loss"],
    },
    {
        "question": "How do antibiotics work against bacteria?",
        "relevant_keywords": ["antibiotic", "bacteria", "infection"],
    },
    {
        "question": "What are common symptoms of anxiety disorders?",
        "relevant_keywords": ["anxiety", "panic", "nervous"],
    },
    {
        "question": "What are the warning signs of appendicitis?",
        "relevant_keywords": ["appendicitis", "abdominal pain", "appendix"],
    },
    {
        "question": "What is the difference between osteoarthritis and rheumatoid arthritis?",
        "relevant_keywords": ["arthritis", "joint", "inflammation"],
    },
    {
        "question": "What causes atherosclerosis?",
        "relevant_keywords": ["atherosclerosis", "plaque", "artery"],
    },
    {
        "question": "What are the characteristics of autism spectrum disorder?",
        "relevant_keywords": ["autism", "developmental", "social"],
    },
    {
        "question": "What are common causes of lower back pain?",
        "relevant_keywords": ["back pain", "spine", "vertebrae"],
    },
    {
        "question": "What is Bell's palsy and what causes it?",
        "relevant_keywords": ["bell's palsy", "facial nerve", "paralysis"],
    },
    {
        "question": "What is a biopsy used for?",
        "relevant_keywords": ["biopsy", "tissue sample", "diagnosis"],
    },
    {
        "question": "What are the mood patterns in bipolar disorder?",
        "relevant_keywords": ["bipolar", "mania", "depression"],
    },
    {
        "question": "What is considered high blood pressure?",
        "relevant_keywords": ["blood pressure", "hypertension", "systolic"],
    },
    {
        "question": "What are the symptoms of bronchitis?",
        "relevant_keywords": ["bronchitis", "cough", "mucus"],
    },
    {
        "question": "How are burns classified by severity?",
        "relevant_keywords": ["burn", "degree", "skin damage"],
    },
    # Add more (question, relevant_keywords) pairs from your actual PDF content
]

K = 3  # how many chunks you retrieve per query (matches db.similarity_search k=3)


def is_chunk_relevant(chunk_text: str, keywords: list[str]) -> bool:
    """A chunk counts as relevant if it contains any of the labeled keywords."""
    text_lower = chunk_text.lower()
    return any(kw.lower() in text_lower for kw in keywords)


def evaluate_manual_metrics():
    precisions, recalls, hits, reciprocal_ranks = [], [], [], []

    for item in TEST_SET:
        question = item["question"]
        keywords = item["relevant_keywords"]

        results = db.similarity_search(question, k=K)
        relevance_flags = [is_chunk_relevant(doc.page_content, keywords) for doc in results]

        num_relevant_retrieved = sum(relevance_flags)
        precision_at_k = num_relevant_retrieved / K
        # Recall here assumes at least 1 relevant chunk exists in the corpus;
        # for a stricter recall you'd need to know the TOTAL relevant chunks
        # in the full vectordb (harder to compute, optional extension below).
        recall_at_k = 1.0 if num_relevant_retrieved > 0 else 0.0
        hit = 1 if num_relevant_retrieved > 0 else 0

        # Mean Reciprocal Rank: 1 / rank of first relevant chunk
        rr = 0.0
        for rank, is_rel in enumerate(relevance_flags, start=1):
            if is_rel:
                rr = 1 / rank
                break

        precisions.append(precision_at_k)
        recalls.append(recall_at_k)
        hits.append(hit)
        reciprocal_ranks.append(rr)

        print(f"Q: {question}")
        print(f"  Retrieved {num_relevant_retrieved}/{K} relevant chunks | "
              f"Precision@{K}={precision_at_k:.2f} | RR={rr:.2f}")

    print("\n=== Aggregate Manual Retrieval Metrics ===")
    print(f"Mean Precision@{K}: {sum(precisions)/len(precisions):.3f}")
    print(f"Hit Rate:           {sum(hits)/len(hits):.3f}")
    print(f"Mean Reciprocal Rank: {sum(reciprocal_ranks)/len(reciprocal_ranks):.3f}")


# ---------------------------------------------------------------------------
# 2. RAGAS METRICS (automated, LLM-judged, fully local via Ollama)
# ---------------------------------------------------------------------------
def evaluate_with_ragas():
    import ollama
    from datasets import Dataset
    from langchain_ollama import ChatOllama, OllamaEmbeddings
    from ragas import evaluate
    from ragas.metrics import (
        answer_relevancy,
        context_precision,
        context_recall,
        faithfulness,
    )

    rows = []
    for item in TEST_SET:
        question = item["question"]
        docs = db.similarity_search(question, k=K)
        contexts = [d.page_content for d in docs]

        prompt = f"Answer only from context.\n\nContext:\n{chr(10).join(contexts)}\n\nQuestion:\n{question}"
        response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
        answer = response["message"]["content"]

        rows.append({
            "question": question,
            "contexts": contexts,
            "answer": answer,
            # ground_truth is optional but improves context_recall accuracy;
            # write a short correct answer yourself per question if you have time
            "ground_truth": item.get("ground_truth", answer),
        })

    dataset = Dataset.from_list(rows)

    judge_llm = ChatOllama(model="mistral")
    judge_embeddings = OllamaEmbeddings(model="mistral")

    result = evaluate(
        dataset,
        metrics=[context_precision, context_recall, faithfulness, answer_relevancy],
        llm=judge_llm,
        embeddings=judge_embeddings,
    )

    print("\n=== RAGAS Metrics (LLM-judged) ===")
    print(result)


if __name__ == "__main__":
    evaluate_manual_metrics()
    evaluate_with_ragas()
    # Uncomment once `pip install ragas datasets langchain-ollama` is done:
    # evaluate_with_ragas()