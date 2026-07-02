from enum import StrEnum

from pydantic import BaseModel, Field


class ConfidenceLevel(StrEnum):
    low = "low"
    medium = "medium"
    high = "high"


class RiskFactor(BaseModel):
    name: str = Field(..., examples=["Concentration"])
    severity: ConfidenceLevel = Field(..., description="Relative severity of the risk signal.")
    explanation: str


class RecommendedAction(BaseModel):
    label: str = Field(..., examples=["Review allocation"])
    rationale: str
    priority: ConfidenceLevel = Field(..., description="Relative priority for user review.")


class PortfolioAsset(BaseModel):
    symbol: str = Field(..., examples=["ETH"])
    allocation_percent: float = Field(..., ge=0, le=100)
    estimated_value_usd: float | None = Field(default=None, ge=0)


class PortfolioAnalysisRequest(BaseModel):
    wallet_address: str | None = Field(default=None)
    chain_id: int | None = Field(default=None, ge=1)
    assets: list[PortfolioAsset] = Field(default_factory=list)
    include_recommendations: bool = True


class PortfolioAnalysisResponse(BaseModel):
    analysis_id: str
    summary: str
    risk_score: int = Field(..., ge=0, le=100)
    confidence: ConfidenceLevel
    risk_factors: list[RiskFactor]
    recommended_actions: list[RecommendedAction]
    disclaimer: str


class TokenAnalysisRequest(BaseModel):
    token_address: str | None = Field(default=None)
    symbol: str | None = Field(default=None, examples=["VAL"])
    chain_id: int | None = Field(default=None, ge=1)
    include_contract_signals: bool = True


class TokenAnalysisResponse(BaseModel):
    analysis_id: str
    token_symbol: str
    summary: str
    risk_score: int = Field(..., ge=0, le=100)
    confidence: ConfidenceLevel
    risk_factors: list[RiskFactor]
    recommended_actions: list[RecommendedAction]
    disclaimer: str
