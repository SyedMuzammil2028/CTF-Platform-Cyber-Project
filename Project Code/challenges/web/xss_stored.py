
from flask import render_template, request, make_response

FLAG = "DNCTF{st0r3d_xss_c00kie}"

def register(app, get_db):
    @app.route("/web/xss_stored", methods=["GET", "POST"])
    def xss_stored():
        conn = get_db()
        conn.row_factory = lambda cursor, row: {"id": row[0], "content": row[1]}
        cur = conn.cursor()

        info = None
        if request.method == "POST":
            content = request.form.get("content", "")
            cur.execute("INSERT INTO comments (content) VALUES (?)", (content,))
            conn.commit()
            info = "Comment posted."

        cur.execute("SELECT id, content FROM comments ORDER BY id DESC")
        comments = cur.fetchall()

        resp = make_response(render_template("web/xss_stored.html", comments=comments, info=info))
        resp.set_cookie("admin_flag", FLAG)
        return resp
