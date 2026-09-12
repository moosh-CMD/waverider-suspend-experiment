"""
Disposable experiment app -- NOT part of the waverider repo.

Purpose: observe, directly and unambiguously, what Render's Suspend
action actually does to a running process (SIGTERM+grace vs. immediate
kill), and which commit's code is running after a Resume. Every
observation is a plain stdout log line with a fixed, greppable prefix.
"""

import http.server
import os
import signal
import sys

VERSION = "A"
PID = os.getpid()

print(f"STARTUP version={VERSION} pid={PID}", flush=True)


def handle_sigterm(signum, frame):
    print(f"SIGTERM_RECEIVED version={VERSION} pid={PID}", flush=True)
    sys.exit(0)


signal.signal(signal.SIGTERM, handle_sigterm)


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(VERSION.encode())

    def log_message(self, fmt, *args):
        print(f"REQUEST {self.address_string()} - {fmt % args}", flush=True)


port = int(os.environ.get("PORT", "10000"))
server = http.server.HTTPServer(("0.0.0.0", port), Handler)
print(f"LISTENING port={port} version={VERSION} pid={PID}", flush=True)
server.serve_forever()
