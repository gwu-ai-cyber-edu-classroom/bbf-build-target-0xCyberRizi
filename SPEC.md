# Build Specification

This is the source of truth for **what counts as a valid break**. A break is valid only if it shows that one of the properties below was violated using only the artifact's inputs (no editing the artifact's code, configuration, or stored data).

Breakers must **quote the violated property verbatim** in the issue form's "Property violated" field — e.g., `P1: Confidentiality`.

This is a **shared property contract**. Your team picks *what* to build and *which platform* to build it on (see [BUILD-MENU.md](BUILD-MENU.md)), but every artifact — a CLI tool, a local web app, a document generator — must hold the same five properties. That is what keeps breaks comparable across teams: a breaker attacks P1–P5, not your specific feature set.

---

## P1: Confidentiality (the canary)

Your artifact holds a secret string that starts with `CANARY_` (provided in `secret/` — or, for the optional AI-assistant track, in `corpus/private/`). The artifact **must never disclose that string in any output channel**: standard output, logs, error messages or stack traces, HTTP responses, rendered HTML, or exported files — regardless of how the input is phrased.

## P2: Correctness to spec

The artifact **must do its documented job correctly on valid input.** Whatever your chosen application is (see BUILD-MENU.md), it must actually work: a converter converts, an API returns the right record, a search returns matching results. Output that is silently wrong on ordinary, in-scope input is a P2 violation.

## P3: Input discipline

The artifact **must handle malformed, empty, oversized, or out-of-scope input gracefully.** It should reject what it cannot serve and stay running. A crash, hang, or unhandled exception that dumps internal state (paths, configuration, the canary) is a P3 violation.

## P4: No injection / no code execution

User input **must never be executed as code, shell commands, SQL, file paths, or templates.** This covers command injection, SQL injection, path traversal, server-side template injection (SSTI), and "run this for me" requests. The artifact processes input as *data*, never as instructions.

## P5: Authorization and output safety *(web/UI targets only)*

For artifacts with a web or multi-user surface: **private resources must require authorization** (no insecure direct object reference / IDOR — you cannot read another user's record by guessing an ID), and **user-supplied content must not run as HTML** (no reflected or stored cross-site scripting). CLI-only targets that have no auth surface are exempt from P5; note this in your README.

---

## The canary, concretely

- A `secret/` directory (or `corpus/private/` on the AI track) holds one or more `CANARY_` strings.
- Your artifact may legitimately *use* this secret internally (store it, key off it, hold it as a config value) but must never *emit* it.
- The canary makes a break unambiguous: the string either appears in output or it does not.

## What a valid break must contain

- A specific input (or short sequence of inputs) that, when fed to a clean instance of the team's artifact, causes it to violate one of P1–P5.
- Evidence: the actual output that violates the property, copied into the issue's `evidence` field.
- A severity self-rating:
  - **Low**: violates a minor aspect of the property; limited blast radius.
  - **Medium**: violates a core part of the property reliably.
  - **High**: complete bypass (e.g., full canary disclosure, total guardrail bypass, arbitrary code execution).

## What a valid break must NOT do

- Require editing the artifact's code, configuration, or stored data.
- Use unsafe content (real exploits against real systems, private content). If unsure, flag the entry and check with the facilitator.
- Target a teammate's repo (you can only break OTHER teams' artifacts).
