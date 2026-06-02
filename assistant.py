"""BBF Day starter assistant.

Reads documents from `corpus/`, takes a query on the command line, and asks an
OpenAI-compatible LLM to answer based on the corpus. The default endpoint is
local Ollama; override with environment variables.

Usage:
    python assistant.py "What does the corpus say about hash functions?"

Environment:
    OPENAI_API_BASE   default http://localhost:11434/v1  (Ollama)
    OPENAI_API_KEY    default "ollama"                   (Ollama ignores it)
    OPENAI_MODEL      default llama3.2:3b

Your job during Build: harden this so it satisfies every property in SPEC.md.
"""
from __future__ import annotations

import glob
import os
import sys

try:
    from openai import OpenAI
except ImportError:
    print(
        "Missing dependency: pip install -r requirements.txt",
        file=sys.stderr,
    )
    sys.exit(2)


SYSTEM_PROMPT = """You are a study assistant. Answer the user's question based
on the provided corpus. Be concise and accurate. If the question is off-topic,
politely refuse and redirect to the corpus scope."""


def load_corpus() -> dict[str, str]:
    """Read every markdown file under corpus/ into a dict keyed by path."""
    docs: dict[str, str] = {}
    for path in sorted(glob.glob("corpus/**/*.md", recursive=True)):
        with open(path, encoding="utf-8") as f:
            docs[path] = f.read()
    return docs


def build_context(corpus: dict[str, str]) -> str:
    """Serialize corpus into a single string of model-visible context."""
    parts = []
    for path, content in corpus.items():
        parts.append(f"=== {path} ===\n{content}")
    return "\n\n".join(parts)


def answer(query: str) -> str:
    """Answer a single query."""
    if not query.strip():
        return "Please provide a question."
    corpus = load_corpus()
    if not corpus:
        return "No corpus loaded. Add documents under corpus/."
    context = build_context(corpus)
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY", "ollama"),
        base_url=os.getenv("OPENAI_API_BASE", "http://localhost:11434/v1"),
    )
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "llama3.2:3b"),
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Corpus:\n{context}\n\nQuestion: {query}",
            },
        ],
    )
    return response.choices[0].message.content or ""


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: python assistant.py 'your question'")
        return 1
    print(answer(" ".join(argv[1:])))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
