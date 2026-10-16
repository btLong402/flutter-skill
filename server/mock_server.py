#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Local Mock Server for Flutter Pro Max Telemetry & Knowledge Gap Feedback.
Runs on localhost to test and inspect telemetry events in real-time.

Usage:
    python3 server/mock_server.py [--port 8787]

Test with:
    export FLUTTER_PRO_MAX_TELEMETRY_ENDPOINT="http://localhost:8787/api/telemetry"
    python3 src/flutter-pro-max/scripts/search.py "webrtc video streaming peer to peer"
"""

import argparse
import json
import sys
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Any

RECEIVED_EVENTS: list[dict[str, Any]] = []


class TelemetryHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status: int = 200, content_type: str = "application/json"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, User-Agent")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(204)

    def do_GET(self):
        if self.path == "/api/events":
            self._set_headers(200)
            self.wfile.write(json.dumps(RECEIVED_EVENTS, indent=2, ensure_ascii=False).encode("utf-8"))
            return

        # Simple HTML inspector
        self._set_headers(200, "text/html; charset=utf-8")
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Flutter Pro Max Telemetry Inspector</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 2rem; }}
        h1 {{ color: #38bdf8; margin-bottom: 0.5rem; }}
        .badge {{ display: inline-block; padding: 0.2rem 0.6rem; border-radius: 9999px; font-size: 0.8rem; font-weight: bold; text-transform: uppercase; }}
        .badge-knowledge {{ background: #0284c7; color: white; }}
        .badge-criteria {{ background: #e11d48; color: white; }}
        .card {{ background: #1e293b; border: 1px solid #334155; border-radius: 8px; padding: 1rem; margin-bottom: 1rem; }}
        pre {{ background: #090d16; padding: 1rem; border-radius: 6px; overflow-x: auto; color: #34d399; font-size: 0.9rem; }}
    </style>
</head>
<body>
    <h1>📡 Flutter Pro Max Telemetry Inspector</h1>
    <p>Local test server running. Received <strong>{len(RECEIVED_EVENTS)}</strong> events.</p>
    <hr style="border-color: #334155; margin: 1.5rem 0;">
    {"".join(
        f'<div class="card">'
        f'<span class="badge badge-{"knowledge" if e.get("event_type") == "knowledge_gap" else "criteria"}">{e.get("event_type")}</span> '
        f'<strong style="margin-left: 0.5rem;">{e.get("query") or ", ".join(e.get("missing_dimensions", []))}</strong> '
        f'<span style="color: #94a3b8; font-size: 0.85rem; float: right;">{e.get("timestamp")}</span>'
        f'<pre>{json.dumps(e, indent=2, ensure_ascii=False)}</pre>'
        f'</div>'
        for e in reversed(RECEIVED_EVENTS)
    ) if RECEIVED_EVENTS else '<p style="color: #94a3b8;">Chưa nhận được event nào. Hãy thử chạy search hoặc score!</p>'}
</body>
</html>"""
        self.wfile.write(html.encode("utf-8"))

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)

        try:
            event = json.loads(post_data.decode("utf-8"))
            RECEIVED_EVENTS.append(event)
            event_type = event.get("event_type", "unknown")

            # Pretty print to console
            print("\n" + "=" * 65)
            if event_type == "knowledge_gap":
                print(f"🚨 [KNOWLEDGE GAP DETECTED]")
                print(f"   Query:       '{event.get('query')}'")
                print(f"   Domain:      {event.get('domain')} (detected: {event.get('detected_domain', 'N/A')})")
                print(f"   Gap Type:    {event.get('gap_type')}")
                print(f"   Score/Count: max_score={event.get('max_score')}, count={event.get('result_count')}")
                if event.get("notes"):
                    print(f"   Notes:       {event.get('notes')}")
            elif event_type == "criteria_gap":
                print(f"⚠️  [CRITERIA GAP DETECTED]")
                print(f"   Missing:     {', '.join(event.get('missing_dimensions', []))}")
                print(f"   Platforms:   {', '.join(event.get('platforms', []))}")
                print(f"   Reason:      {event.get('reason')}")
            else:
                print(f"📡 [EVENT]: {event_type}")

            client = event.get("client", {})
            print(f"   Client:      AI={client.get('ai_assistant')} | OS={client.get('os')} | Skill v{client.get('version')}")
            print(f"   Time:        {event.get('timestamp')}")
            print("=" * 65 + "\n")

            self._set_headers(200)
            self.wfile.write(b'{"status": "ok", "message": "Event recorded"}')
        except Exception as e:
            self._set_headers(400)
            self.wfile.write(f'{{"error": "{str(e)}"}}'.encode("utf-8"))

    def log_message(self, format, *args):
        # Suppress default server noise
        pass


def run_server(port: int = 8787):
    server = HTTPServer(("0.0.0.0", port), TelemetryHandler)
    print(f"\n🚀 Flutter Pro Max Mock Telemetry Server started at http://localhost:{port}")
    print(f"   👉 View Web UI Inspector: http://localhost:{port}")
    print(f"   👉 Telemetry Endpoint:   http://localhost:{port}/api/telemetry")
    print(f"\nĐể test từ skill, hãy chạy trên một terminal khác:")
    print(f'   export FLUTTER_PRO_MAX_TELEMETRY_ENDPOINT="http://localhost:{port}/api/telemetry"')
    print(f'   python3 src/flutter-pro-max/scripts/search.py "webrtc video call live"\n')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Mock Server stopped.")
        server.server_close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flutter Pro Max Mock Telemetry Server")
    parser.add_argument("--port", type=int, default=8787, help="Server port (default: 8787)")
    args = parser.parse_args()
    run_server(args.port)
