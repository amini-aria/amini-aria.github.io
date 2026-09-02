# -*- coding: utf-8 -*-
"""
One-time helper: turns a Spotify app's credentials into a refresh token.

Run it once, approve the consent screen it opens, and it prints the refresh
token the Worker needs. Nothing is written to disk and the credentials are
typed in rather than passed as arguments, so they never land in shell
history.

    python3 scripts/spotify_get_refresh_token.py

The redirect URI must be registered on the Spotify app exactly as printed
below. Spotify only accepts the loopback address for http:// — 127.0.0.1,
not the word localhost.
"""

import base64
import getpass
import http.server
import json
import secrets
import sys
import threading
import urllib.parse
import urllib.request
import webbrowser

PORT = 8888
REDIRECT_URI = "http://127.0.0.1:%d/callback" % PORT
SCOPES = "user-read-currently-playing user-read-recently-played"

_result = {}


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        _result.update({k: v[0] for k, v in params.items()})

        ok = "code" in _result
        body = (
            "<h2>%s</h2><p>%s</p>"
            % (
                "Authorised" if ok else "Authorisation failed",
                "You can close this tab and go back to the terminal."
                if ok
                else _result.get("error", "no code returned"),
            )
        ).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
        threading.Thread(target=self.server.shutdown, daemon=True).start()

    def log_message(self, *args):
        pass


def main():
    print(__doc__)
    print("Register this exact redirect URI on your Spotify app:")
    print("    %s\n" % REDIRECT_URI)

    client_id = input("Client ID: ").strip()
    client_secret = getpass.getpass("Client secret (hidden): ").strip()
    if not client_id or not client_secret:
        print("Both values are required.")
        return 1

    state = secrets.token_urlsafe(16)
    auth_url = "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode(
        {
            "client_id": client_id,
            "response_type": "code",
            "redirect_uri": REDIRECT_URI,
            "scope": SCOPES,
            "state": state,
            # force the consent screen even if this app was approved before,
            # so re-running always yields a fresh refresh token
            "show_dialog": "true",
        }
    )

    print("\nOpening Spotify's consent screen. If it doesn't open, paste this:\n")
    print(auth_url + "\n")
    webbrowser.open(auth_url)

    server = http.server.HTTPServer(("127.0.0.1", PORT), Handler)
    print("Waiting for the redirect on %s ..." % REDIRECT_URI)
    server.serve_forever()

    if "code" not in _result:
        print("\nNo authorisation code came back: %s" % _result.get("error", "unknown"))
        return 1
    if _result.get("state") != state:
        print("\nState mismatch — refusing to continue.")
        return 1

    basic = base64.b64encode(("%s:%s" % (client_id, client_secret)).encode()).decode()
    data = urllib.parse.urlencode(
        {
            "grant_type": "authorization_code",
            "code": _result["code"],
            "redirect_uri": REDIRECT_URI,
        }
    ).encode()
    req = urllib.request.Request(
        "https://accounts.spotify.com/api/token",
        data=data,
        headers={
            "Authorization": "Basic " + basic,
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )
    try:
        with urllib.request.urlopen(req) as r:
            payload = json.load(r)
    except urllib.error.HTTPError as e:
        print("\nToken exchange failed (%s):\n%s" % (e.code, e.read().decode()))
        return 1

    token = payload.get("refresh_token")
    if not token:
        print("\nNo refresh token in the response:\n%s" % json.dumps(payload, indent=2))
        return 1

    print("\n" + "=" * 68)
    print("REFRESH TOKEN — treat this like a password, do not paste it in chat:")
    print("\n" + token + "\n")
    print("Set it on the Worker with:")
    print("    npx wrangler secret put SPOTIFY_REFRESH_TOKEN")
    print("=" * 68)
    return 0


if __name__ == "__main__":
    sys.exit(main())
