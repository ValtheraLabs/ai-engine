from app.schemas.analysis import (
    ConfidenceLevel,
    PortfolioAnalysisRequest,
    PortfolioAnalysisResponse,
    RecommendedAction,
    RiskFactor,
    TokenAnalysisRequest,
    TokenAnalysisResponse,
)

DISCLAIMER = (
    "Mock analysis for product development only. This is not financial advice, "
    "does not guarantee outcomes, and cannot execute transactions."
)


def analyze_portfolio(request: PortfolioAnalysisRequest) -> PortfolioAnalysisResponse:
    largest_allocation = max(
        (asset.allocation_percent for asset in request.assets),
        default=0,
    )
    has_concentration = largest_allocation >= 50

    risk_factors = [
        RiskFactor(
            name="Concentration",
            severity=ConfidenceLevel.high if has_concentration else ConfidenceLevel.medium,
            explanation=(
                "One asset represents at least half of the submitted portfolio."
                if has_concentration
                else "No single submitted asset exceeds half of the portfolio."
            ),
        ),
        RiskFactor(
            name="Data completeness",
            severity=ConfidenceLevel.medium if request.assets else ConfidenceLevel.high,
            explanation=(
                "Risk scoring is based only on the assets supplied to this mock endpoint."
            ),
        ),
    ]

    actions: list[RecommendedAction] = []
    if request.include_recommendations:
        actions.append(
            RecommendedAction(
                label="Review allocation",
                rationale="Validate concentration, liquidity, and personal risk tolerance before acting.",
                priority=ConfidenceLevel.medium,
            )
        )

    return PortfolioAnalysisResponse(
        analysis_id="mock-portfolio-analysis",
        summary="Structured mock portfolio analysis completed.",
        risk_score=72 if has_concentration else 38,
        confidence=ConfidenceLevel.medium,
        risk_factors=risk_factors,
        recommended_actions=actions,
        disclaimer=DISCLAIMER,
    )


def analyze_token(request: TokenAnalysisRequest) -> TokenAnalysisResponse:
    symbol = request.symbol or "UNKNOWN"
    risk_factors = [
        RiskFactor(
            name="Contract verification",
            severity=ConfidenceLevel.medium,
            explanation="This mock endpoint does not inspect live contract source or bytecode.",
        ),
        RiskFactor(
            name="Liquidity",
            severity=ConfidenceLevel.medium,
            explanation="Liquidity depth is not connected yet and must be verified externally.",
        ),
    ]
    actions = [
        RecommendedAction(
            label="Verify token data",
            rationale="Review trusted market, liquidity, and contract sources before making decisions.",
            priority=ConfidenceLevel.high,
        )
    ]

    return TokenAnalysisResponse(
        analysis_id="mock-token-analysis",
        token_symbol=symbol,
        summary=f"Structured mock token analysis completed for {symbol}.",
        risk_score=55,
        confidence=ConfidenceLevel.low,
        risk_factors=risk_factors,
        recommended_actions=actions,
        disclaimer=DISCLAIMER,
    )
