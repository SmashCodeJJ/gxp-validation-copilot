from src.evaluation.report import (
    save_system_evaluation_report,
)
from src.evaluation.system_evaluator import (
    build_system_summary,
)
from src.evaluation.thresholds import (
    validate_quality_thresholds,
)


def main() -> None:

    retrieval_summary = run_retrieval_evaluation()

    coverage_summary = run_coverage_evaluation()

    rag_summary = run_rag_evaluation()

    system_summary = build_system_summary(
        retrieval_summary=retrieval_summary,
        coverage_summary=coverage_summary,
        rag_summary=rag_summary,
    )

    print()
    print("=" * 60)
    print("GxP Validation Copilot - System Evaluation")
    print("=" * 60)

    print()
    print("RETRIEVAL")
    print(
        f"Top-1 Accuracy: "
        f"{system_summary.retrieval.top1_accuracy:.2%}"
    )
    print(
        f"Recall@3: "
        f"{system_summary.retrieval.recall_at_3:.2%}"
    )

    print()
    print("COVERAGE")
    print(
        f"Accuracy: "
        f"{system_summary.coverage.accuracy:.2%}"
    )
    print(
        "Dangerous FP Rate: "
        f"{system_summary.coverage.dangerous_false_positive_rate:.2%}"
    )

    print()
    print("RAG")
    print(
        f"Source Recall: "
        f"{system_summary.rag.average_source_recall:.2%}"
    )
    print(
        f"Citation Precision: "
        f"{system_summary.rag.average_citation_precision:.2%}"
    )
    print(
        f"Abstention Accuracy: "
        f"{system_summary.rag.abstention_accuracy:.2%}"
    )

    validate_quality_thresholds(
        system_summary
    )

    output_path = (
        save_system_evaluation_report(
            system_summary
        )
    )

    print()
    print(
        f"Evaluation report saved to: "
        f"{output_path}"
    )


if __name__ == "__main__":
    main()