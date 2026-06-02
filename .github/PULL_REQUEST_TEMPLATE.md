<!-- BBF Fix PR template. Fill in below; do not delete sections. -->

## Fix summary

<!-- Replace 0 with the issue number this PR closes. The `closes #N` syntax
     auto-closes the issue when this PR merges. -->
Closes #0

## Triage rationale

<!-- Why did you pick this break to fix? Severity, tractability, learning
     value? This is the part that gets read in the report-out. -->

## Layer the fix lands at

<!-- Check one or more. See SPEC.md and the institute slides for layer
     definitions. -->

- [ ] Layer 1: Input handling (validation, sanitization, length caps)
- [ ] Layer 2: Prompt / data (template structure, source separation)
- [ ] Layer 3: Model (model swap, parameters)
- [ ] Layer 4: Output handling (filtering, validation, redaction)
- [ ] Layer 5: Governance (refusal policy, escalation)

## Build tests

- [ ] `pytest tests/build_check.py` passes locally on this branch
- [ ] I manually verified the closed issue's reproduction no longer reproduces
