import json
from unittest.mock import MagicMock

import httpx
import pytest
from pytest import MonkeyPatch

from app.schemas.analysis import (
    PortfolioAnalysisRequest,
    PortfolioAsset,
    TokenAnalysisRequest,
)
from app.services.analysis import analyze_portfolio, analyze_token


def test_portfolio_analysis_uses_llm(monkeypatch: MonkeyPatch) -> None:
    llm_response = json.dumps({
        "summary": "Portfolio is well-diversified across 3 assets.",
        "risk_score": 25,
        "confidence": "medium",
        "risk_factors": [
            {"name": "Diversification", "severity": "low", "explanation": "No single asset dominates."},
        ],
        "recommended_actions": [
            {"label": "Maintain allocation", "rationale": "Current distribution looks balanced.", "priority": "low"},
        ],
    })

    def mock_post(url: str, **kwargs: object) -> MagicMock:
        resp = MagicMock(spec=httpx.Response)
        resp.status_code = 200
        resp.json.return_value = {"response": llm_response}
        resp.raise_for_status = MagicMock()
        return resp

    monkeypatch.setattr("httpx.post", mock_post)

    request = PortfolioAnalysisRequest(
        wallet_address="0x123",
        chain_id=1,
        assets=[
            PortfolioAsset(symbol="ETH", allocation_percent=40, estimated_value_usd=4000),
            PortfolioAsset(symbol="USDC", allocation_percent=30, estimated_value_usd=3000),
            PortfolioAsset(symbol="WBTC", allocation_percent=30, estimated_value_usd=3000),
        ],
    )
    result = analyze_portfolio(request)

    assert result.risk_score == 25
    assert result.confidence == "medium"
    assert len(result.risk_factors) == 1
    assert result.summary == "Portfolio is well-diversified across 3 assets."
    assert "financial advice" in result.disclaimer


def test_portfolio_analysis_falls_back_when_llm_unavailable(
    monkeypatch: MonkeyPatch,
) -> None:
    def mock_post(url: str, **kwargs: object) -> MagicMock:
        raise httpx.ConnectError("connection refused", request=MagicMock())

    monkeypatch.setattr("httpx.post", mock_post)

    request = PortfolioAnalysisRequest(
        wallet_address="0x123",
        chain_id=1,
        assets=[
            PortfolioAsset(symbol="ETH", allocation_percent=60, estimated_value_usd=6000),
        ],
    )
    result = analyze_portfolio(request)

    assert result.risk_score == 72
    assert "concentration" in result.summary.lower()


def test_token_analysis_uses_llm(monkeypatch: MonkeyPatch) -> None:
    llm_response = json.dumps({
        "summary": "Token shows moderate risk. Contract is verified but liquidity is thin.",
        "risk_score": 55,
        "confidence": "low",
        "risk_factors": [
            {"name": "Liquidity", "severity": "medium", "explanation": "Low liquidity depth on DEXes."},
            {"name": "Contract", "severity": "low", "explanation": "Contract source is verified."},
        ],
        "recommended_actions": [
            {"label": "Check liquidity", "rationale": "Verify liquidity before trading.", "priority": "high"},
        ],
    })

    def mock_post(url: str, **kwargs: object) -> MagicMock:
        resp = MagicMock(spec=httpx.Response)
        resp.status_code = 200
        resp.json.return_value = {"response": llm_response}
        resp.raise_for_status = MagicMock()
        return resp

    monkeypatch.setattr("httpx.post", mock_post)

    request = TokenAnalysisRequest(
        token_address="0xabc",
        symbol="VAL",
        chain_id=1,
    )
    result = analyze_token(request)

    assert result.risk_score == 55
    assert result.token_symbol == "VAL"
    assert len(result.risk_factors) == 2


def test_token_analysis_fallback_when_llm_unavailable(
    monkeypatch: MonkeyPatch,
) -> None:
    def mock_post(url: str, **kwargs: object) -> MagicMock:
        raise httpx.ConnectError("connection refused", request=MagicMock())

    monkeypatch.setattr("httpx.post", mock_post)

    request = TokenAnalysisRequest(
        token_address="0xabc",
        symbol="VAL",
        chain_id=1,
    )
    result = analyze_token(request)

    assert result.risk_score == 55
    assert result.analysis_id.startswith("fallback-")
