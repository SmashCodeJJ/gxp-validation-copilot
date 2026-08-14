from src.evaluation.coverage_models import (
    CoverageEvaluationSummary,
)
from src.evaluation.rag_models import (
    RagEvaluationSummary,
)
from src.evaluation.retrieval_models import (
    RetrievalEvaluationSummary,
)
from src.evaluation.system_models import (
    SystemEvaluationSummary,
)


def build_system_summary(
    retrieval_summary: RetrievalEvaluationSummary,
    coverage_summary: CoverageEvaluationSummary,
    rag_summary: RagEvaluationSummary,
) -> SystemEvaluationSummary:

    return SystemEvaluationSummary(
        retrieval=retrieval_summary,
        coverage=coverage_summary,
        rag=rag_summary,
    )