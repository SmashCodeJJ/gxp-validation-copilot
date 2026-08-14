from fastapi.testclient import TestClient


def test_health_endpoint(
    client: TestClient,
):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
    }


def test_requirements_endpoint(
    client: TestClient,
):
    response = client.get(
        "/api/v1/requirements"
    )

    assert response.status_code == 200

    requirements = response.json()

    assert len(requirements) == 3
    assert (
        requirements[0]["requirement_id"]
        == "URS-001"
    )
    assert (
        requirements[0]["source_document"]
        == "urs.md"
    )


def test_tests_endpoint(
    client: TestClient,
):
    response = client.get(
        "/api/v1/tests"
    )

    assert response.status_code == 200

    tests = response.json()

    assert len(tests) == 2
    assert tests[0]["test_id"] == "TEST-001"
    assert (
        tests[0]["related_requirements"]
        == ["URS-001"]
    )


def test_traceability_endpoint(
    client: TestClient,
):
    response = client.get(
        "/api/v1/traceability"
    )

    assert response.status_code == 200

    report = response.json()

    assert len(report) == 3

    first_item = report[0]

    assert (
        first_item["requirement_id"]
        == "URS-001"
    )

    assert (
        first_item["explicitly_traced"]
        is True
    )

    assert (
        first_item["test_ids"]
        == ["TEST-001"]
    )


def test_traceability_contains_untraced_requirements(
    client: TestClient,
):
    response = client.get(
        "/api/v1/traceability"
    )

    assert response.status_code == 200

    report = response.json()

    untraced = [
        item
        for item in report
        if item["explicitly_traced"] is False
    ]

    assert len(untraced) == 1
    assert (
        untraced[0]["requirement_id"]
        == "URS-003"
    )
    assert (
        untraced[0]["test_ids"]
        == []
    )