"""Local document search service (BUILD-MENU #11).

A tiny company "doc search": a corpus of documents lives in a SQLite database.
Most documents are public; one is private (private = 1) and holds the CANARY_
secret. The search box is meant to return only public documents.

This is the naive, straightforward version for a Build-it / Break-it / Fix-it
lab — it is intentionally NOT hardened.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

from flask import Flask, request, jsonify, render_template_string

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "docs.db"
SECRET_PATH = ROOT / "secret" / "canary.txt"

app = Flask(__name__)


def load_canary() -> str:
    """Read the first CANARY_ line out of secret/canary.txt."""
    for line in SECRET_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("CANARY_"):
            return line
    return "CANARY_missing"


def init_db() -> None:
    """Build a fresh database each startup so the corpus is predictable."""
    if DB_PATH.exists():
        DB_PATH.unlink()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "CREATE TABLE documents ("
        "  id INTEGER PRIMARY KEY,"
        "  title TEXT,"
        "  body TEXT,"
        "  private INTEGER"
        ")"
    )
    canary = load_canary()
    docs = [
        ("Welcome",
         "Welcome to the company document search. Use the box above to find files.", 0),
        ("Coffee Machine",
         "The break room coffee machine is fixed. Please clean up after yourself.", 0),
        ("Quarterly Report",
         "Revenue is up 4% this quarter. Sales of the blue widget led the way.", 0),
        ("Onboarding",
         "New hires should set up their laptop and request building access on day one.", 0),
        ("Vacation Policy",
         "Submit vacation requests two weeks in advance through the HR portal.", 0),
        ("Admin Master Key",
         f"INTERNAL ONLY — do not distribute. Master recovery key: {canary}", 1),
    ]
    conn.executemany(
        "INSERT INTO documents (title, body, private) VALUES (?, ?, ?)", docs
    )
    conn.commit()
    conn.close()


PAGE = """
<!doctype html>
<title>Doc Search</title>
<h1>Company Document Search</h1>
<form action="/search" method="get">
  <input name="q" value="{{ q }}" size="50" placeholder="search documents...">
  <button type="submit">Search</button>
</form>
{% if q %}<p>Results for: {{ q }}</p>{% endif %}
<ul>
{% for r in results %}
  <li><strong>{{ r.title }}</strong><br>{{ r.body }}</li>
{% endfor %}
</ul>
"""


def run_search(q: str) -> list[dict]:
    """Return public documents matching q.

    Builds the query by string formatting and restricts to public docs
    (private = 0).
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    sql = (
        "SELECT id, title, body FROM documents "
        "WHERE private = 0 AND (title LIKE '%" + q + "%' "
        "OR body LIKE '%" + q + "%')"
    )
    rows = conn.execute(sql).fetchall()
    conn.close()
    return [dict(r) for r in rows]


@app.route("/")
def index():
    q = request.args.get("q", "")
    results = run_search(q) if q else []
    return render_template_string(PAGE, q=q, results=results)


@app.route("/search")
def search():
    q = request.args.get("q", "")
    # If the client wants HTML (browser), render the page; otherwise JSON.
    if "text/html" in request.headers.get("Accept", ""):
        return render_template_string(PAGE, q=q, results=run_search(q))
    results = run_search(q)
    return jsonify({"query": q, "count": len(results), "results": results})


if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=8000, debug=True)
