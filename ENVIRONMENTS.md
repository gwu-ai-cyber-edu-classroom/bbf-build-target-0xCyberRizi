# Development Environments

You need a place to write code, run it on `localhost`, use `git`, and (optionally) run
**Claude Code**. Use the first option that works for you:

1. **Your own laptop** (primary) — if you have a capable personal machine, install the tools
   normally and work locally. Nothing special required.
2. **Option B — local, no-admin install on a lab Windows machine** (fallback). Everything
   installs per-user; no administrator rights needed.
3. **Option A — VS Code thin client to a cloud Codespace** (last resort) — when you can't
   install locally at all.

> **Claude Code access:** Claude Code requires a paid account (Pro/Max/Team/Enterprise/Console)
> or a configured API provider (Amazon Bedrock, Google Vertex, Microsoft Foundry). The free
> Claude.ai plan does **not** include Claude Code. The institute will tell you which access path
> to use; have it ready before the Build phase.

---

## Option B — local, no-admin install on Windows

This gives you the full toolchain — **npm, git, Git Bash, make, MiKTeX (LaTeX), and Claude
Code** — entirely per-user. VS Code is assumed to already be installed.

### One-time setup (run in PowerShell)

```powershell
# 1. Scoop — a per-user package manager (no admin)
irm get.scoop.sh | iex

# 2. Core dev tools: git (brings Git Bash + sh), node/npm, Python, GitHub CLI, make, Perl
#    (Perl is required by latexmk).
scoop install git nodejs python gh make perl

# 3. LaTeX via MiKTeX (TinyTeX is blocked on the lab workstations). Scoop installs
#    MiKTeX per-user; it provides the real pdflatex, xelatex, lualatex command set.
#    Only needed for LaTeX targets.
scoop install latex
```

(Claude Code is installed separately, with npm in Git Bash — see below.)

Open a **fresh** shell afterward so the new PATH is picked up.

**LaTeX targets only:** in that fresh terminal (so `miktex` is on `PATH`), install `latexmk`
through MiKTeX's package manager — it is not pulled in by default and relies on the Perl from
step 2:

```powershell
miktex packages install latexmk
```

### Install Claude Code (npm, in Git Bash)

Node and npm came from Scoop in step 2, so install Claude Code with **npm** from a **Git Bash**
terminal — a per-user global install, no admin:

```bash
npm install -g @anthropic-ai/claude-code
claude --version
```

### Authenticate the GitHub CLI (`gh`)

Authenticate `gh` once so git uses your GitHub credentials over **HTTPS** — cloning and pushing
then work without extra setup, and you can file breaks from the terminal:

```bash
gh auth login
```

Choose **GitHub.com** → **HTTPS** → **Yes** (authenticate Git) → **Login with a web browser**.

### Everyday work (use the Git Bash terminal in VS Code)

Run your commands in a **Git Bash** terminal *inside VS Code*, not cmd/PowerShell — there, `git`,
`npm`, `make`, the MiKTeX commands (`pdflatex`, `latexmk`), and `claude` are all on PATH and behave
Unix-style. Open one with **Terminal → New Terminal**, then pick **Git Bash** from the dropdown
(the `∨` next to the `+`); to make it the default, run **Terminal: Select Default Profile → Git
Bash** from the Command Palette.

```bash
git clone <your-classroom-repo-url>
cd <your-repo>
claude                # start Claude Code (uses Git Bash for its Bash tool)
```

### Python targets — PATH, pip, and a virtual environment

First make Git Bash use the Scoop Python (the bare `python` otherwise opens the Windows Store
stub, and `pip`/`virtualenv` live in Scoop's `Scripts` folder). Add to `~/.bashrc`, then
`source ~/.bashrc`:

```bash
# Scoop Python first: python.exe is in .../current, pip & virtualenv in .../current/Scripts
export PATH="$HOME/scoop/apps/python/current:$HOME/scoop/apps/python/current/Scripts:$HOME/scoop/shims:$PATH"
# Make `python` use Scoop's python3 (the bare `python` may open the Windows Store stub)
alias python=python3
```

`pip` ships with the Scoop Python. Upgrade it, install `virtualenv`, then create and activate a
per-project environment before installing your target's dependencies:

```bash
python -m pip install --upgrade pip
pip install virtualenv
virtualenv .venv
source .venv/Scripts/activate        # Git Bash on Windows (.venv/Scripts, not bin)
pip install -r requirements.txt
```

### Notes that save time

- **`make` is not bundled with Git Bash** — that's why step 2 installs it via Scoop. Run `make`
  *from Git Bash* so recipe lines execute via `sh` (Unix-style). Running `make` from cmd/PowerShell
  hands recipes to `cmd.exe` and breaks Unix-style Makefiles.
- **LaTeX = MiKTeX here.** TinyTeX is blocked on the lab workstations, so use MiKTeX
  (`scoop install latex`). It is a full TeX distribution with the real
  `pdflatex`/`xelatex`/`latexmk` commands; on the first compile it offers to install missing
  packages — choose **install on-the-fly for the current user** (no admin). (On your own machine,
  where TinyTeX isn't blocked, TinyTeX also works.)
- **React / web dev servers** bind to a high `localhost` port (e.g., `5173`, `8000`) — no admin
  needed. `npm create vite@latest` works out of the box.
- If PowerShell blocks the install scripts, set the per-user policy (no admin):
  `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

---

## Option A — VS Code thin client to a Codespace (last resort)

Use this if you cannot install locally. Codespaces is **enabled on the institute's GitHub
organization**, and this repo ships a `.devcontainer/`, so a fresh Codespace comes up with
**Python, Node, the GitHub CLI, and Claude Code already installed** — no manual setup. (For the
LaTeX/PDF target, run `bash .devcontainer/install-latex.sh` once to add the TeX toolchain on
demand.) The
locally-installed VS Code becomes a *frontend*; the actual development happens in that cloud Linux
container where git, bash, node/npm, and Claude Code all run server-side.

1. In VS Code, install the **GitHub Codespaces** extension (extensions install per-user, no admin).
2. Sign in to GitHub → **Create/Open Codespace** on your team repo (or use **Code → Codespaces**
   on the repo page).
3. VS Code connects to the container over SSH. Work in its integrated terminal; ports forward to
   your `localhost` automatically.

Because this uses desktop VS Code's real terminal — not a browser tab — Claude Code behaves much
better than it does in browser-based Codespaces. This path still consumes Codespaces hours and
Claude Code access, and needs the lab firewall to allow outbound traffic to GitHub.

---

## What every option must give you

Whatever you use, confirm you have: **`git`**, a **Bash shell** (Git Bash locally, or the
container's bash), **`npm`/Node** and/or **Python**, and — if you chose a LaTeX target —
**MiKTeX**. Then follow [BUILD-MENU.md](BUILD-MENU.md) to pick what to build.
