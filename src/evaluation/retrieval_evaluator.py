from src.evaluation.models import (
    RetrievalEvaluationResult,
    RetrievalEvaluationSummary,
)


class RetrievalEvaluator:

    def evaluate_requirement(
        self,
        requirement_id: str,
        expected_test_id: str,
        predicted_test_ids: list[str],
    ) -> RetrievalEvaluationResult:

        top1_correct = (
            len(predicted_test_ids) > 0
            and predicted_test_ids[0] == expected_test_id
        )

        top3_correct = (
            expected_test_id
            in predicted_test_ids[:3]
        )

        return RetrievalEvaluationResult(
            requirement_id=requirement_id,
            expected_test_id=expected_test_id,
            predicted_test_ids=predicted_test_ids,
            top1_correct=top1_correct,
            top3_correct=top3_correct,
        )

    def summarize(
        self,
        results: list[RetrievalEvaluationResult],
    ) -> RetrievalEvaluationSummary:

        if not results:
            raise ValueError(
                "Evaluation results cannot be empty."
            )

        total = len(results)

        top1_correct_count = sum(
            result.top1_correct
            for result in results
        )

        top3_correct_count = sum(
            result.top3_correct
            for result in results
        )

        return RetrievalEvaluationSummary(
            total_requirements=total,
            top1_accuracy=top1_correct_count / total,
            recall_at_3=top3_correct_count / total,
            results=results,
        )