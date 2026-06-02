#!/usr/bin/env bash
# On-demand LaTeX toolchain for the LaTeX/PDF report target (BUILD-MENU.md #25).
# Run this ONLY if your team is building that target:
#
#     bash .devcontainer/install-latex.sh
#
# It installs TeX Live (pdflatex, xelatex, latexmk) into the container. This takes
# a few minutes and ~1 GB, which is why it is not part of the default container
# build — keeping every other team's Codespace launch fast.
set -euo pipefail

echo "==> Installing LaTeX toolchain (a few minutes, ~1 GB)..."
sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
  texlive-latex-recommended \
  texlive-latex-extra \
  texlive-fonts-recommended \
  latexmk
sudo rm -rf /var/lib/apt/lists/*

echo "==> LaTeX ready:"
pdflatex --version | head -1 || true
latexmk --version  | head -1 || true
