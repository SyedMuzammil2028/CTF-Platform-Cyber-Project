
from flask import render_template, request

def register(app, get_db):
    @app.route("/web/csrf_easy", methods=["GET", "POST"])
    def csrf_easy():
        message = None
        if request.method == "POST":
            email = request.form.get("email", "")
            conn = get_db()
            cur = conn.cursor()
            # No CSRF protection, directly updates csrf_victim
            cur.execute("UPDATE users SET email = ? WHERE username = 'csrf_victim'", (email,))
            conn.commit()
            # Fetch flag for the victim user
            cur.execute("SELECT flag FROM users WHERE username = 'csrf_victim'")
            row = cur.fetchone()
            flag = row[0] if row else None
            message = f"Email updated for csrf_victim. Flag: {flag}"
        return render_template("web/csrf_easy.html", message=message)
