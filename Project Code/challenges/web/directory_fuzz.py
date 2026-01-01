
from flask import render_template

def register(app, get_db):
    @app.route("/web/directory_fuzz", methods=["GET"])
    def directory_fuzz():
        # Info-only challenge; flag lives at /hidden/flag_dir.txt
        return render_template("web/directory_fuzz.html")

    @app.route("/hidden/flag_dir.txt")
    def hidden_flag_dir():
        # Real flag file exposed via unlinked path
        return "DNCTF{d1r_fuzz_r3v34ls_s3cr3ts}\n"
