from pydantic import BaseModel

from src.evaluation.coverage_models import (
    CoverageEvaluationSummary,
)
from src.evaluation.rag_models import (
    RagEvaluationSummary,
)
from src.evaluation.retrieval_models import (
    RetrievalEvaluationSummary,
)


class SystemEvaluationSummary(BaseModel):

    retrieval: RetrievalEvaluationSummary

    coverage: CoverageEvaluationSummary

    rag: RagEvaluationSummary