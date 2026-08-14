import csv
import os
from pathlib import Path
from time import perf_counter

from dotenv import load_dotenv

from src.database.session import SessionLocal
from src.evaluation.rag_evaluator import (
    evaluate_rag_case,
    summarize_rag_results,
)
from src.LLM.rag_answerer import RagAnswerer
from src.semantic.embedding_service import EmbeddingService
from src.services.rag_retrieval_service import (
    RagRetrievalService,
)
from src.services.rag_service import RagService


load_dotenv()


GROUND_TRUTH_PATH = (
    "data/evaluation/rag_ground_truth.csv"
)


def parse_source_ids(
    raw_value: str,
) -> list[str]:
    """
    Convert a CSV value such as:

        URS-010|TEST-006

    into:

        ["URS-010", "TEST-006"]

    An empty value becomes an empty list.
    """

    if not raw_value:
        return []

    if not raw_value.strip():
        return []

    return [
        source_id.strip()
        for source_id in raw_value.split("|")
        if source_id.strip()
    ]


def parse_boolean(
    raw_value: str,
) -> bool:
    """
    Convert the CSV string "true" or "false"
    into a Python boolean.
    """

    return raw_value.strip().lower() == "true"


def main() -> None:
    print()
    print("Starting RAG evaluation...")

    # -----------------------------------------
    # 1. Create embedding service
    # -----------------------------------------

    embedding_service = EmbeddingService()

    # -----------------------------------------
    # 2. Create retrieval service
    # -----------------------------------------

    retrieval_service = RagRetrievalService(
        embedding_service=embedding_service
    )

    # -----------------------------------------
    # 3. Create LLM answerer
    # -----------------------------------------

    model_name = os.getenv(
        "OPENAI_MODEL",
        "gpt-5-mini",
    )

    answerer = RagAnswerer(
        model_name=model_name
    )

    # -----------------------------------------
    # 4. Create complete RAG service
    # -----------------------------------------

    rag_service = RagService(
        retrieval_service=retrieval_service,
        answerer=answerer,
    )

    # -----------------------------------------
    # 5. Open database session
    # -----------------------------------------

    session = SessionLocal()

    evaluation_results = []

    try:
        ground_truth_file = Path(
            GROUND_TRUTH_PATH
        )

        if not ground_truth_file.exists():
            raise FileNotFoundError(
                f"Ground truth file not found: "
                f"{GROUND_TRUTH_PATH}"
            )

        # -----------------------------------------
        # 6. Read evaluation questions
        # -----------------------------------------

        with ground_truth_file.open(
            newline="",
            encoding="utf-8",
        ) as csv_file:

            reader = csv.DictReader(
                csv_file
            )

            for row_number, row in enumerate(
                reader,
                start=1,
            ):
                question = row[
                    "question"
                ].strip()

                expected_source_ids = (
                    parse_source_ids(
                        row.get(
                            "expected_source_ids",
                            "",
                        )
                    )
                )

                answerable = parse_boolean(
                    row.get(
                        "answerable",
                        "false",
                    )
                )

                print()
                print("-" * 60)
                print(
                    f"Question {row_number}: "
                    f"{question}"
                )
                print(
                    f"Expected sources: "
                    f"{expected_source_ids}"
                )
                print(
                    f"Answerable: "
                    f"{answerable}"
                )

                # ---------------------------------
                # 7. Run retrieval separately
                # ---------------------------------

                retrieved_documents = (
                    retrieval_service.retrieve(
                        session=session,
                        question=question,
                    )
                )

                retrieved_source_ids = [
                    document.source_id
                    for document
                    in retrieved_documents
                ]

                print(
                    f"Retrieved sources: "
                    f"{retrieved_source_ids}"
                )

                # ---------------------------------
                # 8. Measure complete RAG latency
                # ---------------------------------

                start_time = perf_counter()

                rag_answer = (
                    rag_service.answer_question(
                        session=session,
                        question=question,
                    )
                )

                latency_seconds = (
                    perf_counter()
                    - start_time
                )

                # ---------------------------------
                # 9. Extract citations
                # ---------------------------------

                cited_source_ids = [
                    source.source_id
                    for source
                    in rag_answer.sources
                ]

                print(
                    f"Cited sources: "
                    f"{cited_source_ids}"
                )

                print(
                    f"Answer: "
                    f"{rag_answer.answer}"
                )

                print(
                    f"Latency: "
                    f"{latency_seconds:.2f}s"
                )

                # ---------------------------------
                # 10. Evaluate this question
                # ---------------------------------

                result = evaluate_rag_case(
                    question=question,
                    expected_source_ids=(
                        expected_source_ids
                    ),
                    answerable=answerable,
                    retrieved_source_ids=(
                        retrieved_source_ids
                    ),
                    cited_source_ids=(
                        cited_source_ids
                    ),
                    answer=(
                        rag_answer.answer
                    ),
                    latency_seconds=(
                        latency_seconds
                    ),
                )

                evaluation_results.append(
                    result
                )

                print(
                    f"Source Recall: "
                    f"{result.source_recall:.2%}"
                )

                print(
                    f"Citation Precision: "
                    f"{result.citation_precision:.2%}"
                )

                if (
                    result.abstention_correct
                    is not None
                ):
                    print(
                        "Correct abstention: "
                        f"{result.abstention_correct}"
                    )

        # -----------------------------------------
        # 11. Build aggregate evaluation summary
        # -----------------------------------------

        summary = summarize_rag_results(
            evaluation_results
        )

        # -----------------------------------------
        # 12. Print final report
        # -----------------------------------------

        print()
        print("=" * 60)
        print("RAG Evaluation Summary")
        print("=" * 60)

        print(
            f"Questions evaluated: "
            f"{summary.total_questions}"
        )

        print(
            f"Answerable questions: "
            f"{summary.answerable_questions}"
        )

        print(
            f"Unanswerable questions: "
            f"{summary.unanswerable_questions}"
        )

        print()

        print(
            f"Average Source Recall: "
            f"{summary.average_source_recall:.2%}"
        )

        print(
            f"Average Citation Precision: "
            f"{summary.average_citation_precision:.2%}"
        )

        print(
            f"Abstention Accuracy: "
            f"{summary.abstention_accuracy:.2%}"
        )

        print(
            f"Correct Abstentions: "
            f"{summary.correct_abstentions}"
        )

        print()

        print(
            f"Average Latency: "
            f"{summary.average_latency_seconds:.2f}s"
        )

        print(
            f"Maximum Latency: "
            f"{summary.max_latency_seconds:.2f}s"
        )

        print("=" * 60)

    finally:
        session.close()


if __name__ == "__main__":
    main()