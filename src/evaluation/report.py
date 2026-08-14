from datetime import datetime
from pathlib import Path

from src.evaluation.system_models import (
    SystemEvaluationSummary,
)


def save_system_evaluation_report(
    summary: SystemEvaluationSummary,
) -> Path:

    output_directory = Path(
        "reports/evaluation"
    )

    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    output_path = (
        output_directory
        / f"system_evaluation_{timestamp}.json"
    )

    output_path.write_text(
        summary.model_dump_json(
            indent=2
        ),
        encoding="utf-8",
    )

    return output_path