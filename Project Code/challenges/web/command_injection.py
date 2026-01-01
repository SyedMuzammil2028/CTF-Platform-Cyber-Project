import os
import platform
from flask import render_template, request

# Path to flag file (in root folder of project)
# This is mainly for administration/setup, not for the vulnerability itself
FLAG_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "flag_cmd.txt"
)

def register(app, get_db):

    @app.route("/web/command_injection", methods=["GET", "POST"])
    def command_injection():
        output = ""
        error = "" # Ensure you define error for the template

        if request.method == "POST":
            # NOTE: Changed from 'ip' to 'host' to match the HTML form
            ip = request.form.get("host", "").strip() 

            # Auto-detect OS
            system = platform.system().lower()

            if "windows" in system:
                # Windows ping syntax
                # The vulnerability still exists here for Windows metacharacters like '&' or '|'
                cmd = f"ping -n 1 {ip}" 
            else:
                # Linux / Mac - Target for the common payloads
                cmd = f"ping -c 1 {ip}"

            # ---- DELIBERATE COMMAND INJECTION (The core of the challenge) ----
            try:
                # os.popen executes the string as a shell command, making it vulnerable
                stream = os.popen(cmd)
                output = stream.read()
            except Exception as e:
                error = f"Error executing command: {e}"

        # Pass 'error' to template
        return render_template("web/command_injection.html", output=output, error=error)