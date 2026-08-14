from src.ingestion.models import TestCase
from src.semantic.text_builder import (
    build_test_embedding_text,
)


def test_build_test_embedding_text():
    test_case = TestCase(
        test_id="TEST-001",
        objective="Verify authentication.",
        related_requirements=["URS-001"],
        test_steps=[
            "Enter invalid credentials.",
            "Attempt login.",
        ],
        expected_result="Access is denied.",
        source_document="validation_tests.md",
    )

    text = build_test_embedding_text(test_case)

    assert "Verify authentication" in text
    assert "Step 1: Enter invalid credentials" in text
    assert "Access is denied" in text

    # Avoid leaking the explicit traceability label
    assert "URS-001" not in text