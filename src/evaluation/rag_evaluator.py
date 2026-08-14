from src.evaluation.rag_models import (
    RagEvaluationResult,
    RagEvaluationSummary,
)


def calculate_source_recall(
    expected_source_ids: list[str],
    retrieved_source_ids: list[str],
) -> float:
    """
    Calculate how many expected sources were successfully retrieved.

    Example:
        expected = ["URS-008", "TEST-005"]
        retrieved = ["URS-008", "TEST-002", "TEST-005"]

        recall = 2 / 2 = 1.0
    """

    if not expected_source_ids:
        return 1.0

    expected = set(expected_source_ids)
    retrieved = set(retrieved_source_ids)

    found = expected.intersection(retrieved)

    return len(found) / len(expected)


def calculate_citation_precision(
    cited_source_ids: list[str],
    retrieved_source_ids: list[str],
) -> float:
    """
    Calculate the percentage of cited sources that actually existed
    in the retrieved context.

    Example:
        cited = ["URS-008", "TEST-999"]
        retrieved = ["URS-008", "TEST-005"]

        valid citations = ["URS-008"]

        precision = 1 / 2 = 0.5
    """

    if not cited_source_ids:
        return 1.0

    cited = set(cited_source_ids)
    retrieved = set(retrieved_source_ids)

    valid = cited.intersection(retrieved)

    return len(valid) / len(cited)


def detect_abstention(
    answer: str,
) -> bool:
    """
    Detect whether the RAG system refused to invent an answer
    when there was insufficient evidence.

    This is a simple rule-based baseline.
    """

    normalized = answer.lower()

    abstention_phrases = [
        "insufficient",
        "not provided",
        "does not provide",
        "cannot determine",
        "not enough information",
        "not available",
        "unable to determine",
        "no sufficient evidence",
        "insufficient evidence",
    ]

    return any(
        phrase in normalized
        for phrase in abstention_phrases
    )


def evaluate_rag_case(
    question: str,
    expected_source_ids: list[str],
    answerable: bool,
    retrieved_source_ids: list[str],
    cited_source_ids: list[str],
    answer: str,
    latency_seconds: float,
) -> RagEvaluationResult:
    """
    Evaluate one RAG question.

    Measures:
    - source recall
    - citation precision
    - abstention behavior
    - latency
    """

    source_recall = calculate_source_recall(
        expected_source_ids=expected_source_ids,
        retrieved_source_ids=retrieved_source_ids,
    )

    citation_precision = calculate_citation_precision(
        cited_source_ids=cited_source_ids,
        retrieved_source_ids=retrieved_source_ids,
    )

    abstention_correct = None

    if not answerable:
        abstention_correct = detect_abstention(
            answer
        )

    return RagEvaluationResult(
        question=question,
        expected_source_ids=expected_source_ids,
        retrieved_source_ids=retrieved_source_ids,
        cited_source_ids=cited_source_ids,
        answerable=answerable,
        source_recall=source_recall,
        citation_precision=citation_precision,
        abstention_correct=abstention_correct,
        latency_seconds=latency_seconds,
        answer=answer,
    )


def summarize_rag_results(
    results: list[RagEvaluationResult],
) -> RagEvaluationSummary:
    """
    Aggregate individual RAG evaluation results into
    system-level metrics.
    """

    if not results:
        raise ValueError(
            "RAG evaluation results cannot be empty."
        )

    total_questions = len(results)

    average_source_recall = (
        sum(
            result.source_recall
            for result in results
        )
        / total_questions
    )

    average_citation_precision = (
        sum(
            result.citation_precision
            for result in results
        )
        / total_questions
    )

    answerable_questions = sum(
        1
        for result in results
        if result.answerable
    )

    unanswerable_results = [
        result
        for result in results
        if not result.answerable
    ]

    unanswerable_questions = len(
        unanswerable_results
    )

    correct_abstentions = sum(
        1
        for result in unanswerable_results
        if result.abstention_correct is True
    )

    abstention_accuracy = (
        correct_abstentions
        / unanswerable_questions
        if unanswerable_questions > 0
        else 1.0
    )

    average_latency_seconds = (
        sum(
            result.latency_seconds
            for result in results
        )
        / total_questions
    )

    max_latency_seconds = max(
        result.latency_seconds
        for result in results
    )

    return RagEvaluationSummary(
        total_questions=total_questions,
        average_source_recall=average_source_recall,
        average_citation_precision=average_citation_precision,
        answerable_questions=answerable_questions,
        unanswerable_questions=unanswerable_questions,
        correct_abstentions=correct_abstentions,
        abstention_accuracy=abstention_accuracy,
        average_latency_seconds=average_latency_seconds,
        max_latency_seconds=max_latency_seconds,
        results=results,
    )