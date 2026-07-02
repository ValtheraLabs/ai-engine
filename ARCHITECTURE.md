# AI Engine Architecture

## Role

The AI engine is Valthera's intelligence layer. It should produce structured, explainable outputs for portfolio analysis, token research, wallet intelligence, and risk-aware trading assistance.

## Agent Modules

```text
ai-engine
├── Portfolio Agent
├── Risk Agent
├── Token Research Agent
├── Market Agent
├── Wallet Intelligence Agent
├── Trading Assistant Agent
├── Schema Validation
├── Evaluation Harness
└── Provider Gateway
```

## MVP Agent Responsibilities

### Portfolio Agent

Analyzes wallet allocation, concentration, assets, and high-level portfolio health.

### Risk Agent

Explains risk factors such as illiquidity, volatility, concentration, suspicious token behavior, and contract uncertainty.

### Token Research Agent

Summarizes token metadata, holder structure, liquidity, contract signals, and available public context.

### Wallet Intelligence Agent

Analyzes wallet behavior, trading frequency, holding patterns, and exposure.

### Trading Assistant Agent

Explains possible trading actions and risks, but never executes transactions.

## Output Principle

Prefer structured JSON outputs over unstructured prose so frontend and backend systems can display results safely and consistently.

## Example Output Shape

```json
{
  "summary": "High concentration risk detected.",
  "risk_score": 72,
  "factors": [
    {
      "name": "Concentration",
      "severity": "high",
      "explanation": "One asset represents more than 60% of the portfolio."
    }
  ],
  "recommended_next_steps": [
    "Review allocation before increasing exposure."
  ]
}
```

## Safety Boundary

The AI engine can recommend and explain. It cannot sign, submit, or hide blockchain transactions.
