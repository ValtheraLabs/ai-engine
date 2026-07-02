# Valthera AI Engine

The AI engine powers Valthera's portfolio intelligence, token research, wallet analysis, market summaries, and risk-aware trading assistance.

## Purpose

Provide structured, explainable AI outputs for the Valthera web app and backend API.

## MVP Responsibilities

- Portfolio analysis
- Token research summaries
- Wallet intelligence
- Risk scoring explanations
- Market summaries
- AI copilot response generation
- Structured JSON outputs for frontend rendering

## Preferred Stack

- Python
- FastAPI or internal service interface
- Agent graph/orchestration framework
- Provider-agnostic LLM clients
- Evaluation test cases
- Structured schema validation

## Safety Rule

The AI engine must never directly execute transactions. It may analyze, explain, simulate, or recommend. Users must explicitly review and sign all blockchain actions through their wallet.

## First Milestone

Build an AI service skeleton with health check, portfolio analysis stub, token analysis stub, schema definitions, and evaluation examples.

## MVP-005 and MVP-006 Service Skeleton

This repository now includes a Python 3.12+ FastAPI service skeleton with structured mock analysis endpoints.

### Stack

- Python 3.12+
- FastAPI
- Uvicorn
- Pydantic
- Pytest

### Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` if local configuration overrides are needed. Do not add LLM API keys, private keys, wallet secrets, or transaction credentials.

### Run

```bash
uvicorn app.main:app --reload
```

### Test

```bash
pytest
```

### Endpoints

- `GET /health`
- `POST /v1/analyze/portfolio`
- `POST /v1/analyze/token`

Example portfolio request:

```json
{
  "wallet_address": "0x0000000000000000000000000000000000000000",
  "chain_id": 1,
  "assets": [
    {
      "symbol": "ETH",
      "allocation_percent": 60,
      "estimated_value_usd": 6000
    }
  ]
}
```

Example token request:

```json
{
  "token_address": "0x0000000000000000000000000000000000000000",
  "symbol": "VAL",
  "chain_id": 1
}
```

### Safety Boundaries

- Mock JSON only.
- No real LLM API keys.
- No private keys.
- No transaction execution.
- No financial advice claims.
- Users must verify all analysis before acting.
