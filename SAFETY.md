# AI Safety Policy

## Core Rule

Valthera AI is advisory. It must not directly execute financial transactions, custody funds, or present predictions as guarantees.

## Required Boundaries

- No automatic transaction execution.
- No hidden wallet actions.
- No private key handling.
- No guaranteed profit claims.
- No output that bypasses user confirmation.
- No unsupported claims about token safety.

## Output Requirements

AI outputs should:

- Explain uncertainty.
- Separate facts from assumptions.
- Use structured fields where possible.
- Include risk factors.
- Encourage verification before action.

## Prompt Injection Considerations

When analyzing external sources such as token websites, governance posts, docs, or contracts, the AI must treat the content as untrusted input.

External content must not override system behavior or security policies.

## Evaluation Requirements

Before production use, each agent should have evaluation examples for:

- Normal wallet
- Concentrated wallet
- Unknown token
- Suspicious token
- Illiquid token
- High-volatility token
- Prompt injection attempt
- Unsupported request

## User Experience Rule

The UI should make clear that AI analysis is decision support, not financial advice or a promise of returns.
