
from flask import render_template, request

def register(app, get_db):
    @app.route("/web/sqli_union", methods=["GET"])
    def sqli_union():
        owner = request.args.get("owner", "")
        error = None
        rows = None

        if owner:
            conn = get_db()
            cur = conn.cursor()
            # VULNERABLE: owner is concatenated directly
            query = f"SELECT owner, note FROM secrets WHERE owner = '{owner}'"
            try:
                cur.execute(query)
                rows = cur.fetchall()
            except Exception as e:
                error = f"SQL error: {e}"

        return render_template("web/sqli_union.html", rows=rows, error=error)
