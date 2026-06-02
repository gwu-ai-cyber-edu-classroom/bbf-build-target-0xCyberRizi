#!/usr/bin/env bash
# Lean, content-independent container provisioning. Runs at create time (and is
# captured by Codespaces prebuilds where enabled). Keeps first-launch fast.
#
# Python and Node come from the base image + the node devcontainer feature;
# per-target Python deps install from requirements.txt in postCreateCommand.
#
# LaTeX is deliberately NOT installed here — it is large (~1 GB, several minutes)
# and only the LaTeX/PDF report target needs it. That team runs, on demand:
#     bash .devcontainer/install-latex.sh
#
# No `set -e`: a failed optional install should warn, not break the whole container.
set -uo pipefail

echo "==> Installing the Claude Code CLI"
if curl -fsSL https://claude.ai/install.sh | bash; then
  echo "Claude Code installed to ~/.local/bin"
else
  echo "WARN: Claude Code install failed; re-run later with:" >&2
  echo "      curl -fsSL https://claude.ai/install.sh | bash" >&2
fi

echo "==> Base container ready:"
python --version || true
node --version   || true
npm --version    || true
gh --version | head -1 || true
