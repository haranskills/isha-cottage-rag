import os
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from src.agent.graph import rag_agent
from src.config import OPENAI_API_KEY, OPENAI_MODEL, EMBEDDING_MODEL
from src.logger import logger
from tests.eval_dataset import eval_questions


def run_evaluation():
    logger.info("Starting RAGAS evaluation...")

    questions = []
    answers = []
    contexts = []

    for i, question in enumerate(eval_questions, 1):
        logger.info(f"Running question {i}/{len(eval_questions)}: {question}")

        try:
            initial_state = {
                "query": question,
                "retrieved_chunks": [],
                "answer": "",
                "sources": [],
                "conversation_history": []
            }

            result = rag_agent.invoke(
                initial_state,
                config={"recursion_limit": 10}
            )

            questions.append(question)
            answers.append(result["answer"])

            # RAGAS needs contexts as list of strings
            chunk_texts = [
                c.page_content for c in result["retrieved_chunks"]
            ]
            contexts.append(chunk_texts)

            logger.success(f"Q{i} done — answer: {result['answer'][:80]}...")

        except Exception as e:
            logger.error(f"Failed on question {i}: {e}")
            questions.append(question)
            answers.append("Error")
            contexts.append([""])

    # Build RAGAS dataset
    eval_dataset = Dataset.from_dict({
        "question": questions,
        "answer": answers,
        "contexts": contexts,
    })

    # Run evaluation
    logger.info("Scoring with RAGAS...")

    llm = ChatOpenAI(
        model=OPENAI_MODEL,
        openai_api_key=OPENAI_API_KEY
    )
    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        openai_api_key=OPENAI_API_KEY
    )

    results = evaluate(
        dataset=eval_dataset,
        metrics=[faithfulness, answer_relevancy],
        llm=llm,
        embeddings=embeddings
    )

    # Convert to pandas for easy access
    df = results.to_pandas()

    faithfulness_score = df["faithfulness"].mean()
    relevancy_score = df["answer_relevancy"].mean()

    print("\n" + "="*50)
    print("RAGAS EVALUATION RESULTS")
    print("="*50)
    print(f"Faithfulness:      {faithfulness_score:.4f}")
    print(f"Answer Relevancy:  {relevancy_score:.4f}")
    print("="*50)

    # Save results to file
    with open("ragas_results.txt", "w") as f:
        f.write("RAGAS EVALUATION RESULTS\n")
        f.write("="*50 + "\n")
        f.write(f"Model: {OPENAI_MODEL}\n")
        f.write(f"Embedding: {EMBEDDING_MODEL}\n")
        f.write(f"Questions tested: {len(eval_questions)}\n")
        f.write("="*50 + "\n")
        f.write(f"Faithfulness:      {faithfulness_score:.4f}\n")
        f.write(f"Answer Relevancy:  {relevancy_score:.4f}\n")

    logger.success("Results saved to ragas_results.txt")
    return results


if __name__ == "__main__":
    run_evaluation()