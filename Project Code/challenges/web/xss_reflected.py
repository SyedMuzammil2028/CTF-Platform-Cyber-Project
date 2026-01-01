
from flask import render_template, request, make_response

FLAG = "DNCTF{r3fl3ct3d_xss_m1rr0r}"

def register(app, get_db):
    @app.route("/web/xss_reflected", methods=["GET"])
    def xss_reflected():
        q = request.args.get("q")
        resp = make_response(render_template("web/xss_reflected.html", query=q))
        # Flag hidden in cookie like a typical stolen-cookie scenario
        resp.set_cookie("refxss_flag", FLAG)
        return resp
