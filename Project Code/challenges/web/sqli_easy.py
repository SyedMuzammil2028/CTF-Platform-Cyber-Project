
from flask import render_template, request
import sqlite3

FLAG = "DNCTF{simpl3_sql_inj3cti0n}"

def register(app, get_db):
    @app.route("/web/sqli_easy", methods=["GET", "POST"])
    def sqli_easy():
        error = None
        flag = None
        if request.method == "POST":
            username = request.form.get("username", "")
            password = request.form.get("password", "")

            conn = get_db()
            cur = conn.cursor()
            # VULNERABLE: password concatenated directly into SQL
            query = f"SELECT id, username FROM users WHERE username = ? AND password = '{password}'"
            try:
                cur.execute(query, (username,))
                row = cur.fetchone()
            except sqlite3.Error as e:
                error = f"SQL error: {e}"
                row = None

            if row:
                flag = FLAG
            else:
                if not error:
                    error = "Login failed."
        return render_template("web/sqli_easy.html", error=error, flag=flag)
