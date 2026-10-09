"""Minimal GitHub OAuth provider for Sveltia CMS, serving Boardify."""
import json
import os
import secrets
from urllib.parse import urlencode

import requests
from dotenv import load_dotenv
from flask import Flask, abort, redirect, render_template_string, request, session, url_for

load_dotenv()

CLIENT_ID = os.environ["OAUTH_CLIENT_ID"]
CLIENT_SECRET = os.environ["OAUTH_CLIENT_SECRET"]
SECRET_KEY = os.environ["SECRET_KEY"]
# Origins of the Boardify CMS (comma separated), e.g. https://boardify.app
ALLOWED_ORIGINS = {o.strip().rstrip("/") for o in os.environ["ALLOWED_ORIGINS"].split(",") if o.strip()}
GITHUB_URL = os.environ.get("GIT_HOSTNAME", "https://github.com").rstrip("/")
SCOPE = os.environ.get("SCOPES", "repo,user")

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config.update(SESSION_COOKIE_SAMESITE="Lax", SESSION_COOKIE_SECURE=not app.debug, SESSION_COOKIE_HTTPONLY=True)

# Sveltia/Decap handshake: the popup announces itself, the CMS window replies,
# and only then is the result posted back, targeted at the verified origin.
CALLBACK_PAGE = """<!doctype html><html><body><script>
(function () {
  var allowed = {{ allowed|tojson }};
  var result = {{ result|tojson }};
  window.addEventListener("message", function (e) {
    if (allowed.indexOf(e.origin) === -1) return;
    window.opener.postMessage(result, e.origin);
    window.close();
  });
  window.opener.postMessage("authorizing:github", "*");
})();
</script></body></html>"""


@app.get("/")
def index():
    return "Boardify OAuth provider", 200


@app.get("/auth")
def auth():
    """Redirect the Sveltia CMS popup to GitHub."""
    session["state"] = state = secrets.token_urlsafe(32)
    params = {
        "client_id": CLIENT_ID,
        "scope": request.args.get("scope", SCOPE).replace(",", " "),
        "state": state,
        "redirect_uri": url_for("callback", _external=True),
    }
    return redirect(f"{GITHUB_URL}/login/oauth/authorize?{urlencode(params)}")


@app.get("/callback")
def callback():
    """Exchange the code for a token and hand it to the CMS window."""
    expected = session.pop("state", None)
    if not expected or not secrets.compare_digest(expected, request.args.get("state", "")):
        abort(400, "Invalid state")

    try:
        resp = requests.post(
            f"{GITHUB_URL}/login/oauth/access_token",
            headers={"Accept": "application/json"},
            data={
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "code": request.args.get("code", ""),
                "redirect_uri": url_for("callback", _external=True),
            },
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        if "access_token" not in data:
            raise ValueError(data.get("error_description") or data.get("error") or "No access token")
        status, content = "success", {"token": data["access_token"], "provider": "github"}
    except (requests.RequestException, ValueError) as e:
        status, content = "error", {"message": str(e)}

    result = f"authorization:github:{status}:{json.dumps(content)}"
    return render_template_string(CALLBACK_PAGE, allowed=sorted(ALLOWED_ORIGINS), result=result)


if __name__ == "__main__":
    app.run()
