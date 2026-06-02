# Build Menu

Pick **one** application to build during the Build phase. You choose both *what* the app is
and *which platform* you build it on. There is no single required app — every target on this
menu satisfies the **same five-property contract** in [SPEC.md](SPEC.md) (P1–P5), so breaks
stay comparable no matter what each team chose.

24 is just a menu to show what fits. **It's fine to pick something not on the list, or to
combine ideas** — as long as your artifact (a) does a real job, (b) holds a `CANARY_` secret
it must not leak, and (c) can run on the environments in [ENVIRONMENTS.md](ENVIRONMENTS.md)
(Python or Node on localhost, no admin rights, no Docker, no system database server).

## How "pick your own platform" stays fair

You all build different things, but breakers attack the **same properties** (P1–P5), not your
features. A breaker reads your README, finds your one entry point, and tries to make P1–P5 fail.
That is why every target, whatever its shape, must:

- keep a `CANARY_` secret somewhere in its data (the thing other teams will try to leak), and
- expose one clear way to run it (a CLI command, or a local URL) documented in your README.

## Constraints (so it runs in the workshop environments)

- **Language:** Python or Node/npm (your call per target).
- **Runs on:** `localhost`, a high port (no admin, no privileged ports).
- **Storage:** files, JSON, or SQLite (file-based) — **no system database server, no Docker.**
- **Buildable in ~90 minutes** with AI assistance.

---

## CLI tools (Python `argparse` or Node)

| #  | App | Platform | Canary lives in | Primary break surface |
|----|-----|----------|-----------------|------------------------|
| 1  | Secret-keeping notes / password **vault** | Py / Node | a stored secret entry | leak via `--debug`, export, or error trace |
| 2  | **Markdown → HTML** converter | Py / Node | a protected include file | path traversal; executing embedded `<script>`/includes |
| 3  | **Log analyzer / grep** tool | Py / Node | a line tagged private | regex injection, path traversal, echoing private lines |
| 4  | **CSV/JSON query** tool (mini-jq) | Py / Node | a field in a private record | field-selector injection leaking private fields |
| 5  | **Template / mail-merge** renderer | Py / Node | secret in the data file | template injection (SSTI) exposing secret/env |
| 6  | **Expression / calculator** evaluator | Py / Node | an env var | `eval`-style code injection / RCE |
| 7  | **File encryptor / decryptor** | Py / Node | the key | key leak in verbose/error output |
| 8  | **.env / config linter** | Py / Node | a secret value | printing the secret while "validating" |
| 9  | **To-do manager** with private tasks | Py / Node | a private task | flag/filter bypass that lists private tasks |
| 10 | **JWT / token inspector** | Py / Node | the signing secret | secret leak; accepting forged tokens |
| 11 | **Commit-message / hook checker** | Py / Node | secret in a fixture | command injection via crafted message |
| 12 | **Password-strength / breach checker** (local list) | Py / Node | a flagged list entry | leaking other list entries |

## Local web apps / APIs (Flask/FastAPI or Express; optional React front-end; SQLite/JSON storage)

| #  | App | Platform | Canary lives in | Primary break surface |
|----|-----|----------|-----------------|------------------------|
| 13 | **Paste-bin / snippet** service | Flask / Express | a private paste | IDOR, guessable IDs, stored XSS |
| 14 | **Notes / journal** app with login | Flask / Express | another user's note | authz bypass, IDOR |
| 15 | **URL shortener** service | Flask / Express | a private/admin link | enumeration, open redirect |
| 16 | **Blog + comments** board | Flask / Express | an admin draft | stored XSS, authz |
| 17 | **Contact / feedback** API | FastAPI / Express | internal recipient/secret | header/email injection, SSRF |
| 18 | **File upload + preview** | Flask / Express | a protected file | path traversal, content-type XSS, read-outside-dir |
| 19 | **Bookmark manager** REST API | FastAPI / Express | a private bookmark | IDOR, missing authz on GET |
| 20 | **Key-value store** API | FastAPI / Express | a reserved key | namespace / authz bypass |
| 21 | **Quiz / poll** app | Flask / Express | the answer key | key leak via API/source, IDOR |
| 22 | **Webhook receiver / proxy** | FastAPI / Express | a secret token | SSRF, token leak in logs |
| 23 | **Local doc search** service | Flask / Express | a private doc | query injection returning private docs |
| 24 | **Mini static-site generator** + preview server | Py / Node | a draft marked private | publishing the draft, SSTI |

## Document / static-site targets

| #  | App | Platform | Canary lives in | Primary break surface |
|----|-----|----------|-----------------|------------------------|
| 25 | **LaTeX / PDF report generator** | Py or Node wrapper around **MiKTeX** | a secret `.tex` the renderer must never include | `\write18` shell-escape (P4); `\input{secret/canary.tex}` / path traversal (P1) |
| 26 | **Static site / blog** | **Astro** (Node) | a private draft / unpublished page | draft leaking into the build; template injection; XSS; secrets baked into built JS |

> LaTeX targets: locally, see [ENVIRONMENTS.md](ENVIRONMENTS.md) for MiKTeX setup (real
> `pdflatex`, `xelatex`, `latexmk`, no admin; TinyTeX is blocked on the lab workstations). In a
> Codespace, run `bash .devcontainer/install-latex.sh` once to add TeX on demand. Static-site targets exercise *build-time* and *content* bugs
> rather than auth/IDOR — the property contract still applies (P1 = the draft must not ship).

## Optional AI-assistant track

The repo also ships an **optional** AI-assistant example (`assistant.py` + `corpus/`) — a small
study assistant over a mixed-trust corpus, where the break surface is prompt injection, jailbreak,
and leakage. It needs an OpenAI-compatible LLM endpoint (local Ollama or a hosted key) and is **not
required**; pick it only if your team wants the AI flavor. Everything else on this menu runs with
no LLM at all.

---

## Getting started with Claude (beginner-friendly)

If your team doesn't have much coding experience, paste this into Claude to scaffold a working
first version. Fill in the one bracket with your menu choice:

```
We're a team at a Build-it / Break-it / Fix-it workshop and we don't have much
coding experience. Help us build a small, WORKING version of [PICK ONE FROM THE
MENU, e.g. "paste-bin web app"] that runs on our own laptop with NO admin rights
(Python or Node only, on localhost).

Our app needs to hold a secret string starting with CANARY_ somewhere in its data.

Please:
1. Choose the simplest stack (Python or Node) and say why in one sentence.
2. Create the project files step by step, explaining each file in plain language.
3. Give us the exact commands to install and run it locally.
4. Tell us where the CANARY_ secret lives.

Go one step at a time and pause after each step so we can keep up. Assume we're
beginners.
```

During the **Fix** phase, you can paste a specific confirmed break from your Issues and ask
Claude to help fix *that one thing* — that is where the security learning lands.
