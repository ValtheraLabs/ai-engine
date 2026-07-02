from fastapi import APIRouter

from app.schemas.analysis import (
    PortfolioAnalysisRequest,
    PortfolioAnalysisResponse,
    TokenAnalysisRequest,
    TokenAnalysisResponse,
)
from app.services.analysis import analyze_portfolio, analyze_token

router = APIRouter(tags=["analysis"])


@router.post("/analyze/portfolio", response_model=PortfolioAnalysisResponse)
def portfolio_analysis(request: PortfolioAnalysisRequest) -> PortfolioAnalysisResponse:
    return analyze_portfolio(request)


@router.post("/analyze/token", response_model=TokenAnalysisResponse)
def token_analysis(request: TokenAnalysisRequest) -> TokenAnalysisResponse:
    return analyze_token(request)
