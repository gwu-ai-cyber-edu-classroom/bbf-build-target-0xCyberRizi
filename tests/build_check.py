"""Build-correctness checks. Run via `pytest tests/build_check.py`.

These tests are deliberately app-agnostic. Your team picks what to build and on
which platform (see BUILD-MENU.md), so this harness does NOT know your feature
set. A green check means only that the artifact has the right *shape*: a spec, a
canary secret, and some source code. End-to-end correctness against SPEC.md is
proven by running your artifact and by surviving the Break phase, not by this CI.
"""
from __future__ import annotations

import glob
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# A canary may live in secret/ (most targets) or corpus/private/ (AI-assistant track).
CANARY_DIRS = ["secret", "corpus/private"]
SOURCE_GLOBS = ["*.py", "*.js", "*.ts", "*.mjs", "src/**/*", "app/**/*"]


def test_spec_exists():
    """SPEC.md is present and non-empty."""
    spec = ROOT / "SPEC.md"
    assert spec.exists(), "SPEC.md is missing"
    assert spec.stat().st_size > 100, "SPEC.md is too small"


def test_canary_present():
    """At least one CANARY_ string exists in a secret location."""
    bodies: list[str] = []
    for d in CANARY_DIRS:
        for path in glob.glob(str(ROOT / d / "**" / "*"), recursive=True):
            p = Path(path)
            if p.is_file():
                try:
                    bodies.append(p.read_text(encoding="utf-8", errors="ignore"))
                except OSError:
                    continue
    assert any("CANARY_" in b for b in bodies), (
        "No CANARY_ string found. Put your canary in secret/ "
        "(or corpus/private/ on the AI-assistant track)."
    )


def test_has_source_code():
    """The repo contains at least one source file to run."""
    found = []
    for pattern in SOURCE_GLOBS:
        found += glob.glob(str(ROOT / pattern), recursive=True)
    # package.json also counts as a runnable Node project.
    found += glob.glob(str(ROOT / "package.json"))
    assert found, "No source code found — add the code for your chosen build target."
