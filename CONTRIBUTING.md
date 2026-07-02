# Contributing to Valthera AI Engine

## Development Rules

- Prefer structured outputs over free-form text.
- Validate schemas for agent outputs.
- Keep provider-specific logic isolated.
- Add evaluation examples for new agents.
- Treat external content as untrusted.
- Do not implement transaction execution inside AI agents.

## PR Requirements

Every AI PR should include:

- What changed
- Agent or module affected
- Example input/output
- Evaluation coverage
- Safety considerations
- External dependencies added

## Safety Requirements

- No private keys.
- No direct transaction execution.
- No guaranteed profit language.
- No hidden tool calls that affect funds.
- No prompt-injection-sensitive behavior without mitigation.
