import logging

from fastapi.testclient import TestClient


def test_request_id_header_is_returned(
    client: TestClient,
):
    response = client.get(
        "/health",
        headers={
            "X-Request-ID": "test-request-123",
        },
    )

    assert response.status_code == 200
    assert (
        response.headers["X-Request-ID"]
        == "test-request-123"
    )


def test_request_completion_is_logged(
    client: TestClient,
    caplog,
):
    with caplog.at_level(
        logging.INFO,
        logger="gxp.api.requests",
    ):
        response = client.get(
            "/health",
            headers={
                "X-Request-ID": "log-request-123",
            },
        )

    assert response.status_code == 200
    assert "request_started" in caplog.text
    assert "request_completed" in caplog.text
    assert "method=GET" in caplog.text
    assert "path=/health" in caplog.text
    assert "status_code=200" in caplog.text
    assert "duration_ms=" in caplog.text
    assert "log-request-123" in caplog.text


def test_version_endpoint_exposes_runtime_metadata(
    client: TestClient,
):
    response = client.get("/version")

    assert response.status_code == 200

    body = response.json()

    assert body["app_name"] == "GxP Validation Copilot"
    assert body["version"]
    assert body["environment"]


def test_readiness_endpoint_checks_database(
    client: TestClient,
):
    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ready",
        "database": "ok",
    }
