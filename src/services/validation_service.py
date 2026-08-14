from pathlib import Path

from src.ingestion.protocol_parser import parse_test_cases
from src.ingestion.requirement_parser import (
    parse_requirements,
    read_document,
)
from src.ingestion.traceability_report import build_traceability_report


class ValidationService:
    def __init__(
        self,
        urs_path: str,
        protocol_path: str,
    ) -> None:
        self.urs_path = urs_path
        self.protocol_path = protocol_path

    def get_requirements(self):
        text = read_document(self.urs_path)

        return parse_requirements(
            text=text,
            source_document=Path(self.urs_path).name,
        )

    def get_tests(self):
        text = read_document(self.protocol_path)

        return parse_test_cases(
            text=text,
            source_document=Path(self.protocol_path).name,
        )

    def get_traceability_report(self):
        return build_traceability_report(
            urs_path=self.urs_path,
            protocol_path=self.protocol_path,
        )