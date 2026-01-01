
from flask import render_template, request
import os

BASE_NOTES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "notes")

def register(app, get_db):
    @app.route("/web/path_traversal", methods=["GET"])
    def path_traversal():
        filename = request.args.get("file", "note.txt")
        error = None
        content = None
        try:
            # VULNERABLE: directly joins user input, no sanitization
            target_path = os.path.join(BASE_NOTES_DIR, filename)
            if os.path.isfile(target_path):
                with open(target_path, "r") as f:
                    content = f.read()
            else:
                error = "File not found."
        except Exception as e:
            error = f"Error: {e}"

        return render_template("web/path_traversal.html", content=content, error=error)
