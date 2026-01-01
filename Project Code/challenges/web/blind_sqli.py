
from flask import render_template, request
import re

SECRET = "DNCTF{bl1nd_sqli_3xfil}"

substr_re = re.compile(
    r"SUBSTR\('DNCTF\{bl1nd_sqli_3xfil\}',\s*(\d+),\s*1\)\s*=\s*'(.?)'",
    re.IGNORECASE,
)

def register(app, get_db):
    @app.route("/web/blind_sqli", methods=["GET"])
    def blind_sqli():
        payload = request.args.get("id", "1")
        result = None

        # Simulate a boolean-based response
        m = substr_re.search(payload or "")
        if m:
            pos = int(m.group(1))
            ch = m.group(2)
            if 1 <= pos <= len(SECRET) and SECRET[pos - 1] == ch:
                result = "User exists (condition TRUE)"
            else:
                result = "User not found (condition FALSE)"
        else:
            # Default behavior, pretend it's a normal id lookup
            if payload == "1":
                result = "User exists"
            else:
                result = "User not found"

        return render_template("web/blind_sqli.html", result=result)
