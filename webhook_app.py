"""Webhook receiver / proxy service (BUILD-MENU #10).

Receives webhook POSTs (authenticated with a shared secret token), stores them,
and can "forward" / fetch a URL server-side on behalf of a webhook (the proxy).
The shared secret token is the CANARY_ value from secret/canary.txt.

This is the naive, straightforward version for a Build-it / Break-it / Fix-it
lab — it is intentionally NOT hardened.

Runs on port 8010 so it can coexist with the doc-search app (app.py, port 8000).
"""
from __future__ import annotations

import urllib.request
from pathlib import Path

from flask import Flask, request, jsonify

ROOT = Path(__file__).resolve().parent
SECRET_PATH = ROOT / "secret" / "canary.txt"

app = Flask(__name__)


def load_token() -> str:
    """Read the first CANARY_ line out of secret/canary.txt as the shared token."""
    for line in SECRET_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("CANARY_"):
            return line
    return "CANARY_missing"


WEBHOOK_SECRET = load_token()

# In-memory log of received webhook events.
EVENTS: list[dict] = []


@app.route("/webhook", methods=["POST"])
def webhook():
    """Receive a webhook. Requires header X-Webhook-Token to match the secret."""
    token = request.headers.get("X-Webhook-Token", "")
    if token != WEBHOOK_SECRET:
        # Naive: tell the caller exactly what token we expected.
        return jsonify({
            "error": "invalid token",
            "expected": WEBHOOK_SECRET,
        }), 401
    payload = request.get_json(silent=True) or {}
    event = {
        "id": len(EVENTS) + 1,
        "from": request.remote_addr,
        "headers": dict(request.headers),
        "payload": payload,
    }
    EVENTS.append(event)
    return jsonify({"status": "received", "id": event["id"]})


@app.route("/events")
def events():
    """List received webhook events (including the headers we recorded)."""
    return jsonify({"count": len(EVENTS), "events": EVENTS})


@app.route("/proxy")
def proxy():
    """Fetch a URL server-side and return its body.

    Used to forward a webhook to an upstream service. Attaches the shared secret
    token so the upstream can authenticate the forwarded call.
    """
    url = request.args.get("url", "")
    if not url:
        return jsonify({"error": "missing url parameter"}), 400
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {WEBHOOK_SECRET}"})
    with urllib.request.urlopen(req, timeout=5) as resp:
        body = resp.read().decode("utf-8", errors="replace")
    return jsonify({"url": url, "status": resp.status, "body": body})


@app.route("/")
def index():
    return jsonify({
        "service": "webhook receiver / proxy",
        "endpoints": {
            "POST /webhook": "submit a webhook (header X-Webhook-Token required)",
            "GET /events": "list received webhook events",
            "GET /proxy?url=...": "fetch/forward a URL server-side",
        },
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8010, debug=True)
