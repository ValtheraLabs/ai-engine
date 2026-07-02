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
