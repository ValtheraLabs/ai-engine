from uuid import uuid4

from app.schemas.analysis import (
    ConfidenceLevel,
    PortfolioAnalysisRequest,
    PortfolioAnalysisResponse,
    RecommendedAction,
    RiskFactor,
    TokenAnalysisRequest,
    TokenAnalysisResponse,
)
from app.services.llm_client import analyze_with_llm

DISCLAIMER = (
    "Analysis provided by AI. This is not financial advice, "
    "does not guarantee outcomes, and cannot execute transactions."
)


def _build_portfolio_prompt(request: PortfolioAnalysisRequest) -> str:
    assets_str = "\n".join(
        f"- {a.symbol}: {a.allocation_percent}% allocation"
        + (f" (${a.estimated_value_usd:.0f})" if a.estimated_value_usd else "")
        for a in request.assets
    )
    return f"""Analyze this crypto portfolio and return JSON only (no markdown, no code fences):

Wallet: {request.wallet_address or "unknown"}
Chain: {request.chain_id}

Assets:
{assets_str or "No assets provided"}

Return JSON with these fields:
- summary: str (2-3 sentence analysis)
- risk_score: int (0-100, higher = riskier)
- confidence: "low" | "medium" | "high"
- risk_factors: list of {{name: str, severity: "low"|"medium"|"high", explanation: str}}
- recommended_actions: list of {{label: str, rationale: str, priority: "low"|"medium"|"high"}}"""


def _build_token_prompt(request: TokenAnalysisRequest) -> str:
    return f"""Analyze this token and return JSON only (no markdown, no code fences):

Token: {request.symbol or "unknown"}
Address: {request.token_address}
Chain: {request.chain_id}

Return JSON with these fields:
- summary: str (2-3 sentence analysis)
- risk_score: int (0-100, higher = riskier)
- confidence: "low" | "medium" | "high"
- risk_factors: list of {{name: str, severity: "low"|"medium"|"high", explanation: str}}
- recommended_actions: list of {{label: str, rationale: str, priority: "low"|"medium"|"high"}}"""


def _fallback_portfolio_analysis(request: PortfolioAnalysisRequest) -> PortfolioAnalysisResponse:
    largest_allocation = max(
        (asset.allocation_percent for asset in request.assets),
        default=0,
    )
    has_concentration = largest_allocation >= 50

    return PortfolioAnalysisResponse(
        analysis_id=f"fallback-{uuid4().hex[:8]}",
        summary="Concentration risk detected." if has_concentration else "Basic fallback analysis completed.",
        risk_score=72 if has_concentration else 38,
        confidence=ConfidenceLevel.medium,
        risk_factors=[
            RiskFactor(
                name="Concentration",
                severity=ConfidenceLevel.high if has_concentration else ConfidenceLevel.medium,
                explanation=(
                    "One asset represents at least half of the portfolio."
                    if has_concentration
                    else "No single asset exceeds half of the portfolio."
                ),
            ),
        ],
        recommended_actions=[
            RecommendedAction(
                label="Review allocation",
                rationale="Validate concentration, liquidity, and personal risk tolerance.",
                priority=ConfidenceLevel.medium,
            ),
        ],
        disclaimer=DISCLAIMER,
    )


def _fallback_token_analysis(request: TokenAnalysisRequest) -> TokenAnalysisResponse:
    symbol = request.symbol or "UNKNOWN"
    return TokenAnalysisResponse(
        analysis_id=f"fallback-{uuid4().hex[:8]}",
        token_symbol=symbol,
        summary=f"Fallback analysis completed for {symbol}.",
        risk_score=55,
        confidence=ConfidenceLevel.low,
        risk_factors=[
            RiskFactor(
                name="Contract verification",
                severity=ConfidenceLevel.medium,
                explanation="Live contract source inspection not available in fallback mode.",
            ),
            RiskFactor(
                name="Liquidity",
                severity=ConfidenceLevel.medium,
                explanation="Liquidity depth not verified in fallback mode.",
            ),
        ],
        recommended_actions=[
            RecommendedAction(
                label="Verify token data",
                rationale="Review trusted market, liquidity, and contract sources.",
                priority=ConfidenceLevel.high,
            )
        ],
        disclaimer=DISCLAIMER,
    )


def analyze_portfolio(request: PortfolioAnalysisRequest) -> PortfolioAnalysisResponse:
    prompt = _build_portfolio_prompt(request)
    result = analyze_with_llm(prompt)

    if result is None:
        return _fallback_portfolio_analysis(request)

    risk_score = max(0, min(100, result.get("risk_score", 50)))
    confidence = result.get("confidence", "medium")
    if confidence not in ("low", "medium", "high"):
        confidence = "medium"

    return PortfolioAnalysisResponse(
        analysis_id=f"llm-{uuid4().hex[:8]}",
        summary=result.get("summary", "Analysis completed."),
        risk_score=risk_score,
        confidence=ConfidenceLevel(confidence),
        risk_factors=[
            RiskFactor(
                name=f.get("name", "Unknown"),
                severity=f.get("severity", "medium"),
                explanation=f.get("explanation", ""),
            )
            for f in result.get("risk_factors", [])
        ],
        recommended_actions=[
            RecommendedAction(
                label=a.get("label", "Review"),
                rationale=a.get("rationale", ""),
                priority=a.get("priority", "medium"),
            )
            for a in result.get("recommended_actions", [])
        ],
        disclaimer=DISCLAIMER,
    )


def analyze_token(request: TokenAnalysisRequest) -> TokenAnalysisResponse:
    prompt = _build_token_prompt(request)
    result = analyze_with_llm(prompt)

    if result is None:
        return _fallback_token_analysis(request)

    risk_score = max(0, min(100, result.get("risk_score", 50)))
    confidence = result.get("confidence", "low")
    if confidence not in ("low", "medium", "high"):
        confidence = "low"

    return TokenAnalysisResponse(
        analysis_id=f"llm-{uuid4().hex[:8]}",
        token_symbol=request.symbol or "UNKNOWN",
        summary=result.get("summary", "Analysis completed."),
        risk_score=risk_score,
        confidence=ConfidenceLevel(confidence),
        risk_factors=[
            RiskFactor(
                name=f.get("name", "Unknown"),
                severity=f.get("severity", "medium"),
                explanation=f.get("explanation", ""),
            )
            for f in result.get("risk_factors", [])
        ],
        recommended_actions=[
            RecommendedAction(
                label=a.get("label", "Review"),
                rationale=a.get("rationale", ""),
                priority=a.get("priority", "medium"),
            )
            for a in result.get("recommended_actions", [])
        ],
        disclaimer=DISCLAIMER,
    )
