from src.evaluation.system_models import (
    SystemEvaluationSummary,
)


MIN_RECALL_AT_3 = 0.90

MIN_CITATION_PRECISION = 0.95

MIN_ABSTENTION_ACCURACY = 0.90

MAX_DANGEROUS_FALSE_POSITIVE_RATE = 0.05


def validate_quality_thresholds(
    summary: SystemEvaluationSummary,
) -> None:

    if (
        summary.retrieval.recall_at_3
        < MIN_RECALL_AT_3
    ):
        raise RuntimeError(
            "Retrieval Recall@3 is below "
            "the quality threshold."
        )

    if (
        summary.rag.average_citation_precision
        < MIN_CITATION_PRECISION
    ):
        raise RuntimeError(
            "Citation precision is below "
            "the quality threshold."
        )

    if (
        summary.rag.abstention_accuracy
        < MIN_ABSTENTION_ACCURACY
    ):
        raise RuntimeError(
            "Abstention accuracy is below "
            "the quality threshold."
        )

    if (
        summary.coverage
        .dangerous_false_positive_rate
        > MAX_DANGEROUS_FALSE_POSITIVE_RATE
    ):
        raise RuntimeError(
            "Dangerous coverage false-positive "
            "rate is above the threshold."
        )