> **Superseded — 22 September 2026.** This prototype was made with Codex on 21 September 2026 and is not the method. It has a six-line prompt, five rules and a script that checks the shape of one data file. The full method — the ten requirements, the design loop, the gate criteria, the verifier and the checking tools — is public at **[tmth-studio/forge-cf](https://github.com/tmth-studio/forge-cf)**. Use that. This repository stays only so old links still land somewhere.

# IVE Architecture Engine — prototype

An experimental, portable architecture method for turning a structured venture brief into an auditable architecture candidate, then checking that candidate against explicit published rules.

## Status

**Prototype — not WS1-qualified.** This repository does not claim that an LLM can reliably create a commercially validated or independently expert-verified venture architecture. Forge WS1's qualification test remains open: three consecutive autonomous held-out runs scoring at least 85, clearing both structural gates, and one independent IVE-expert confirmation.

Here, **verified** means: *the supplied artifact passed the versioned, mechanical checks in this repository*. Qualitative judgement, real-world validation, legal review, and expert sign-off remain separate human work.

## What you can do with this

1. Give your LLM `prompts/system.md` and a copy of `examples/synthetic-venture/input.json`.
2. Ask it to return a JSON architecture artifact following `schemas/architecture.schema.json`.
3. Save that output as `architecture.json`.
4. Run `python3 verifier/verify.py architecture.json`.

The verifier writes a report and exits non-zero when a hard rule fails. An LLM must not change `rules/` or `verifier/` for its own output to be called verified.

```bash
python3 verifier/verify.py examples/synthetic-venture/architecture.json
python3 verifier/verify.py architecture.json --report verification-report.json
python3 -m unittest discover -s tests
```

## Repository map

- `schemas/` — input, architecture and report contracts.
- `prompts/` — portable instructions to give a generator LLM.
- `rules/` — the versioned verification policy.
- `engine/` — a small local scaffold for creating an empty architecture package.
- `verifier/` — independent deterministic checks.
- `examples/` — synthetic, non-confidential example inputs and a passing artifact.

## Non-negotiable boundaries

- A generator and verifier are separate roles.
- Every material architecture claim carries evidence or is flagged as an assumption with a test.
- Every requirement traces to a bottleneck, intervention, component and verification record.
- A passing mechanical report is not a market-validation claim.
- Do not upload personal data, client data, credentials, paid-source text, or private Forge records.

## License

MIT. See `LICENSE`.
