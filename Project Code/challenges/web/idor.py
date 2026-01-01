
from flask import render_template, request

def register(app, get_db):
    @app.route("/web/idor", methods=["GET"])
    def idor():
        conn = get_db()
        conn.row_factory = lambda cursor, row: {
            "id": row[0],
            "username": row[1],
            "display_name": row[2],
            "bio": row[3],
            "is_admin": row[4],
            "flag": row[5],
        }
        cur = conn.cursor()

        profile_id = request.args.get("id", "1")
        error = None
        profile = None
        try:
            cur.execute("SELECT id, username, display_name, bio, is_admin, flag FROM profiles WHERE id = ?", (profile_id,))
            profile = cur.fetchone()
            if not profile:
                error = "No such profile."
        except Exception as e:
            error = f"Error: {e}"

        return render_template("web/idor.html", profile=profile, error=error)
