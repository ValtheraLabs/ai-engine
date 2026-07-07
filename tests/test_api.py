from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_portfolio_analysis_returns_structured_mock() -> None:
    response = client.post(
        "/v1/analyze/portfolio",
        json={
            "wallet_address": "0x0000000000000000000000000000000000000000",
            "chain_id": 1,
            "assets": [
                {
                    "symbol": "ETH",
                    "allocation_percent": 60,
                    "estimated_value_usd": 6000,
                }
            ],
        },
    )

    body = response.json()
    assert response.status_code == 200
    assert body["analysis_id"].startswith("fallback-")
    assert body["risk_score"] == 72
    assert body["risk_factors"]
    assert "financial advice" in body["disclaimer"]


def test_token_analysis_returns_structured_mock() -> None:
    response = client.post(
        "/v1/analyze/token",
        json={
            "token_address": "0x0000000000000000000000000000000000000000",
            "symbol": "VAL",
            "chain_id": 1,
        },
    )

    body = response.json()
    assert response.status_code == 200
    assert body["analysis_id"].startswith("fallback-")
    assert body["token_symbol"] == "VAL"
    assert body["risk_factors"]
    assert body["confidence"] == "low"
