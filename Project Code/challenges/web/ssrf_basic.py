
from flask import render_template, request
import requests

def register(app, get_db):
    @app.route("/web/ssrf_basic", methods=["GET"])
    def ssrf_basic():
        url = request.args.get("url", "")
        content = None
        error = None
        if url:
            try:
                # Very simple SSRF: no restriction on internal IPs
                r = requests.get(url, timeout=5)
                content = r.text[:4000]
            except Exception as e:
                error = f"Error fetching URL: {e}"
        return render_template("web/ssrf_basic.html", content=content, error=error)

    @app.route("/internal/ssrf_flag")
    def internal_ssrf_flag():
        return "DNCTF{ssrf_1nt3rnal_r3ach}\n"
