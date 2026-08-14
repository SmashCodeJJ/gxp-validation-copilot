from src.services.validation_service import ValidationService


URS_PATH = "data/synthetic/abfs100/urs.md"
PROTOCOL_PATH = "data/synthetic/abfs100/validation_tests.md"


def test_validation_service_returns_requirements():
    service = ValidationService(
        urs_path=URS_PATH,
        protocol_path=PROTOCOL_PATH,
    )

    requirements = service.get_requirements()

    assert len(requirements) == 12
    assert requirements[0].requirement_id == "URS-001"


def test_validation_service_returns_tests():
    service = ValidationService(
        urs_path=URS_PATH,
        protocol_path=PROTOCOL_PATH,
    )

    tests = service.get_tests()

    assert len(tests) == 6
    assert tests[0].test_id == "TEST-001"


def test_validation_service_returns_traceability():
    service = ValidationService(
        urs_path=URS_PATH,
        protocol_path=PROTOCOL_PATH,
    )

    report = service.get_traceability_report()

    assert len(report) == 12
    assert report[0]["requirement_id"] == "URS-001"
    assert report[0]["explicitly_traced"] is True