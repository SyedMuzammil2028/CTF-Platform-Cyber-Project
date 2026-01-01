
from flask import render_template, request

def register(app, get_db):
    @app.route("/web/auth_bruteforce", methods=["GET", "POST"])
    def auth_bruteforce():
        info = None
        if request.method == "POST":
            username = request.form.get("username", "")
            password = request.form.get("password", "")
            conn = get_db()
            cur = conn.cursor()
            cur.execute(
                "SELECT flag FROM users WHERE username = ? AND password = ?",
                (username, password),
            )
            row = cur.fetchone()
            if row and row[0]:
                info = f"Login success! Flag: {row[0]}"
            else:
                info = "Login failed."
        return render_template("web/auth_bruteforce.html", info=info)

    @app.route("/web/auth_bruteforce_hint")
    def auth_bruteforce_hint():
        # Simple hint route for CTF players
        return "One admin account uses one of the most common passwords from rockyou.txt."
