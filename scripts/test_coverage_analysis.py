import os

from dotenv import load_dotenv

from src.database.session import SessionLocal
from src.LLM.coverage_evaluator import CoverageEvaluator
from src.services.coverage_analysis_service import (
    CoverageAnalysisService,
)


load_dotenv()


def main() -> None:

    model_name = os.getenv(
        "OPENAI_MODEL",
        "gpt-5-mini",
    )

    evaluator = CoverageEvaluator(
        model_name=model_name
    )

    service = CoverageAnalysisService(
        coverage_evaluator=evaluator
    )

    session = SessionLocal()

    try:
        result = service.analyze_requirement(
            session=session,
            requirement_id="URS-001",
            candidate_limit=3,
        )

        print(
            result.model_dump_json(
                indent=2
            )
        )

    finally:
        session.close()


if __name__ == "__main__":
    main()