from tests.traceability import find_missing_requirements


def test_missing_requirements():
    missing = find_missing_requirements(
        "data/synthetic/abfs100/urs.md",
        "data/synthetic/abfs100/validation_tests.md",
    )

    assert "URS-003" in missing
    assert "URS-007" in missing

    assert "URS-001" not in missing
    assert "URS-002" not in missing