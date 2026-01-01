from flask import Flask, render_template, session, jsonify, request, send_from_directory
import sqlite3
import os

from config import SECRET_KEY, DB_PATH


# ------------------ REGISTER IMPORTS ------------------
# WEB
from challenges.web.sqli_easy import register as register_sqli_easy
from challenges.web.sqli_hard import register as register_sqli_union
from challenges.web.blind_sqli import register as register_blind_sqli
from challenges.web.xss_reflected import register as register_xss_reflected
from challenges.web.xss_stored import register as register_xss_stored
from challenges.web.csrf_easy import register as register_csrf_easy
from challenges.web.auth_bruteforce import register as register_auth_bruteforce
from challenges.web.idor import register as register_idor
from challenges.web.directory_fuzz import register as register_directory_fuzz
from challenges.web.path_traversal import register as register_path_traversal
from challenges.web.command_injection import register as register_command_injection
from challenges.web.ssrf_basic import register as register_ssrf_basic


# ------------------ APP INIT ------------------
app = Flask(__name__)
app.secret_key = SECRET_KEY


# ========================================================
#                      CHALLENGES
# ========================================================

CHALLENGES = {

    # ------------------- WEB -------------------
    # done
    "sqli_easy": {
        "id": "sqli_easy",
        "title": "Login of Kira ",
        "category": "Web Exploitation",
        "difficulty": "Easy",
        "author": "Muzammil",
        "description": "Classic SQL injection in a login form.",
        "route": "/web/sqli_easy",
        "flag": "DNCTF{simpl3_sql_inj3cti0n}",
    },

    # done
    "xss_reflected": {
        "id": "xss_reflected",
        "title": "Mirror of Ryuk ",
        "category": "Web Exploitation",
        "difficulty": "Easy",
        "author": "Muzammil",
        "description": "Basic reflected XSS.",
        "route": "/web/xss_reflected",
        "flag": "DNCTF{r3fl3ct3d_xss_m1rr0r}",
    },

    # done
    "directory_fuzz": {
        "id": "directory_fuzz",
        "title": "Old Pages ",
        "category": "Web Exploitation",
        "difficulty": "Easy",
        "author": "Muzammil",
        "description": "Find hidden directories.",
        "route": "/web/directory_fuzz",
        "flag": "DNCTF{d1r_fuzz_r3v34ls_s3cr3ts}",
    },

    # "csrf_easy": {
    #     "id": "csrf_easy",
    #     "title": "Shinigami's Form (CSRF)",
    #     "category": "Web Exploitation",
    #     "difficulty": "Easy",
    #     "author": "Muzammil",
    #     "description": "CSRF attack to modify admin profile.",
    #     "route": "/web/csrf_easy",
    #     "flag": "DNCTF{csrf_st0len_st4te}",
    # },
    
    # done
    "path_traversal": {
        "id": "path_traversal",
        "title": "Pages Between Pages ",
        "category": "Web Exploitation",
        "difficulty": "Easy",
        "author": "Muzammil",
        "description": "LFI to read unintended files.",
        "route": "/web/path_traversal",
        "flag": "DNCTF{lfi_tr4v3rsal_r3ad}",
    },
    
    # done
    "sqli_union": {
        "id": "sqli_union",
        "title": "Union of Justice ",
        "category": "Web Exploitation",
        "difficulty": "Medium",
        "author": "Muzammil",
        "description": "Union-based SQLi.",
        "route": "/web/sqli_union",
        "flag": "DNCTF{sqli_union_owns_the_note}",
    },

    # done
    "xss_stored": {
        "id": "xss_stored",
        "title": "Voices in the Notebook",
        "category": "Web Exploitation",
        "difficulty": "Medium",
        "author": "Muzammil",
        "description": "Stored XSS through comments.",
        "route": "/web/xss_stored",
        "flag": "DNCTF{st0r3d_xss_c00kie}",
    },
    
    # done
    "auth_bruteforce": {
        "id": "auth_bruteforce",
        "title": "Guess My Name",
        "category": "Web Exploitation",
        "difficulty": "Medium",
        "author": "Muzammil",
        "description": "Bruteforce weak admin password.",
        "route": "/web/auth_bruteforce",
        "flag": "DNCTF{brut3_f0rc3_w1ns}",
    },
    
    
    # done
    "idor": {
        "id": "idor",
        "title": "Out of Order",
        "category": "Web Exploitation",
        "difficulty": "Medium",
        "author": "Muzammil",
        "description": "IDOR on profile access.",
        "route": "/web/idor",
        "flag": "DNCTF{idor_unl0ck3d_101}",
    },

    # to be check
    "blind_sqli": {
        "id": "blind_sqli",
        "title": "Silent Oracle ",
        "category": "Web Exploitation",
        "difficulty": "Hard",
        "author": "Muzammil",
        "description": "Boolean-based blind SQLi.",
        "route": "/web/blind_sqli",
        "flag": "DNCTF{bl1nd_sqli_3xfil}",
    },

    "command_injection": {
        "id": "command_injection",
        "title": "Ping of Death Note",
        "category": "Web Exploitation",
        "difficulty": "Hard",
        "author": "Muzammil",
        "description": "Inject command into ping tool.",
        "route": "/web/command_injection",
        "flag": "DNCTF{p1ng_and_p0wn_shell}",
    },

    # to be check
    # "ssrf_basic": {
    #     "id": "ssrf_basic",
    #     "title": "Inner Eye",
    #     "category": "Web Exploitation",
    #     "difficulty": "Hard",
    #     "author": "Muzammil",
    #     "description": "Basic SSRF to internal endpoint.",
    #     "route": "/web/ssrf_basic",
    #     "flag": "DNCTF{ssrf_1nt3rnal_r3ach}",
    # },

    # ------------------- FORENSICS -------------------
    
    # Done
    "f1_basic_strings": {
        "id": "f1_basic_strings",
        "title": "Binary Whispers",
        "category": "Forensics",
        "difficulty": "Easy",
        "author": "Muzammil",
        "description": "Extract strings from binary.",
        "route": None,
        "file": "f1_basic_strings.bin",
        "flag": "DNCTF{binary_whispers}"
    },

    # Done
    "f2_metadata_leak": {
        "id": "f2_metadata_leak",
        "title": "Shinigami Metadata",
        "category": "Forensics",
        "difficulty": "Easy",
        "author": "Muzammil",
        "description": "Find EXIF secrets.",
        "route": None,
        "file": "f2_image_meta.jpg",
        "flag": "DNCTF{3x1f_l34k4g3}"
    },

    "f3_stego_basic": {
        "id": "f3_stego_basic",
        "title": "Voices in the Pixels",
        "category": "Forensics",
        "difficulty": "Easy",
        "author": "Muzammil",
        "description": "LSB Steganography.",
        "route": None,
        "file": "f3_stego.jpg",
        "flag": "DNCTF{st3g0_r3v34ls}"
    },

    # "f4_network_pcap": {
    #     "id": "f4_network_pcap",
    #     "title": "Packets of Truth (PCAP)",
    #     "category": "Forensics",
    #     "difficulty": "Easy",
    #     "author": "Muzammil",
    #     "description": "Analyze packet capture.",
    #     "route": None,
    #     "file": "f4_network.pcap",
    #     "flag": "DNCTF{pcap_analysis_win}"
    # },
    
    # done
    "f04_stego_": {
        "id": "f04_stego_",
        "title": "Needs of Spaghetti",
        "category": "Forensics",
        "difficulty": "Easy",
        "author": "Muzammil",
        "description": "Some hidden Spaghetti..",
        "route": None,
        "file": "f8_no_need.jpg",
        "flag": "DNCTF{SpaghettiSteg}"
    },
    
    # Done
    "f5_Financial_Report_for_ABC_Labs": {
        "id": "f5_Financial_Report_for_ABC_Labs",
        "title": "Redaction Gone Wrong",
        "category": "Forensics",
        "difficulty": "Easy",
        "author": "Muzammil",
        "description": "A PDF with improperly redacted secrets.",
        "route": None,
        "file": "f5_Financial_Report_for_ABC_Labs.pdf",
        "flag": "DNCTF{C4n_Y0u_S33_m3_fully}"
    },
    
    # Done
    "f7_dns_exfil": {
        "id": "f7_dns_exfil",
        "title": "Shadows of DNS",
        "category": "Forensics",
        "difficulty": "Medium",
        "author": "Muzammil",
        "description": "A massive PCAP file has been captured, but the core issue isn't the volume of traffic—it's the subtlety. We suspect a covert channel was used to exfiltrate data by hiding the flag in DNS queries. The malicious traffic is buried under thousands of benign requests.",
        "route": None,
        "file": "f7_covert_dns_challenge.pcap",
        "flag": "DNCTF{Dom41n_i5_5y5t3m}"
    },
    
    # Done
    "f55_log_contains_flag": {
        "id": "f55_log_contains_flag",
        "title": "Too Many Lies",
        "category": "Forensics",
        "difficulty": "Hard",
        "author": "Muzammil",
        "description": """We've captured a massive file from a compromised server. 
        It seems to contain an overwhelming amount of data, possibly millions 
        of lines of seemingly random or irrelevant text. Somewhere within this
        sea of data, a tiny needle—the flag—is hidden.

        The key to solving this challenge is not simply viewing the file,
        as it is far too large, but efficiently filtering and processing 
        the content. The flag's pattern is likely designed to be missed by 
        a simple, generic search. You'll need to master the command line to 
        isolate the signal from the noise..
        
        Be Aware of Fake flags""",
       
        "route": None,
        "file": "f05_log_.txt",
        "flag": "DNCTF{T00_M4NY_L1N3S_D1D_Y0U_GR3P}"
    },
    
    # "f6_log_forensics": {
    #     "id": "f6_log_forensics",
    #     "title": "Trail of Kira (Log Forensics)",
    #     "category": "Forensics",
    #     "difficulty": "Hard",
    #     "author": "Muzammil",
    #     "description": "Recover tampered logs.",
    #     "route": None,
    #     "file": "f6_logs.txt",
    #     "flag": "DNCTF{k1ra_trace_uncovered}"
    # },
    
    # ------------------- OSINT -------------------
    
    "o3_gateway": {
        "id": "o3_gateway",
        "title": "THE YAGAMI PARALLAX",
        "category": "OSINT",
        "difficulty": "Easy",
        "author": "Ahsan",
        "description": "A distorted image of Light Yagami has begun circulating online, uploaded by an account with no history and no explanation. Those who tried tracing it reported that the picture behaves strangely — its origins don’t match any known source, and following its digital fingerprints leads into an unexpected chain of platforms.\n\nRumors say the creator left hints scattered across multiple corners of the web — a mislabeled board, an innocently named file, and a “light” that isn’t Light at all.",
        "route": None,
        "file": "Death_note_edit.jpg",
        # "points": 300,   
        "flag": "DNCTF{th1s_is_the_re3l_l1ght}"
    },
    
    # Done 
    "o1_gateway": {
        "id": "o1_gateway",
        "title": "The Gateway",
        "category": "OSINT",
        "difficulty": "Medium",
        "author": "Ahsan",
        "description": "Identify a Hawaii airport & aircraft.\n\n Flag Format: DNCTF{Airportname_PLANENAME}",
        "route": None,
        "file": "airport_plane_.jpg",
        # "points": 300,   
        "flag": "DNCTF{Kalaeloa_KC135}"
    },
    
    # Done
    "o2_ahsan1": {
        "id": "o2_ahsan1",
        "title": "The Mustached Prodigy",
        "category": "OSINT",
        "difficulty": "Medium",
        "author": "Ahsan",
        "description": """Rumor says Light Yagami altered his identity before carving a trail of digital breadcrumbs. Some claim his final message hides inside the pixels themselves… others whisper that the truth lies with someone who left an oddly timed remark. \n\n Follow the traces he left behind — from the comments that shouldn’t exist, to a doppelgänger with a questionable picture, to the hidden channels only the cooked ones can discover. Somewhere along this chain, the one who praises the mustache carries something encrypted… something only a true investigator can decode.\n\n Find what Light left behind before it disappears""",
        "route": None,
        "file": "lightwithmustache.jpeg",
        # "points": 300,   
        "flag": "DNCTF{05int_1s_ea5y}"
    },
    
    # ------------------- CRYPTO -------------------
    
    # done
    "c01_mose": {
        "id": "c01_mose",
        "title": "Whispers of the Shinigami",
        "category": "Crypto",
        "difficulty": "Easy",
        "author": "Muzammil",
        "description": "A strange message was intercepted — a long sequence of dots and dashes….",
        "file": "c01_m.txt",
        "route": None,
        "flag": "DNCTF{M0R53_TH3_T3L3C0MMUNIC4TI0N_3NC0DING}"
    },
    
    # done
    "c001_shaheer": {
        "id": "c001_shaheer",
        "title": "Base Layers",
        "category": "Crypto",
        "difficulty": "Easy",
        "author": "Shaheer",
        "description": "Can you find the layer pattern?.",
        "file": "c001_shee_ez.txt",
        "route": None,
        "flag": "DNCTF{easy_multi_layer_encode}"
    },
    
    # done
    "c002_shaheer": {
        "id": "c002_shaheer",
        "title": "Prime Suspect I",
        "category": "Crypto",
        "difficulty": "Medium",
        "author": "Shaheer",
        "description": "RSA is the way to go if you know.",
        "file": "c02_shee_mid.txt",
        "route": None,
        "flag": "DNCTF{medium_shared_prime}"
    },
    
    
    # done
    "c1_rsa_shared_prime": {
        "id": "c1_rsa_shared_prime",
        "title": "Prime Suspect II",
        "category": "Crypto",
        "difficulty": "Medium",
        "author": "Muzammil",
        "description": "Two RSA moduli share a prime. Factor them.",
        "file": "c1_rsa_shared_prime.txt",
        "route": None,
        "flag": "DNCTF{shared_prime_exposed}"
    },
    
    
    # done
    "c003_shaheer": {
        "id": "c003_shaheer",
        "title": "Wiener's RSA",
        "category": "Crypto",
        "difficulty": "Medium",
        "author": "Shaheer",
        "description": "Not that Really much of a difference if you ask me, Ain't i right?",
        "file": "c03_shee_med.txt",
        "route": None,
        "flag": "DNCTF{hard_wiener_rsa}"
    },

    "c2_otp_reuse": {
        "id": "c2_otp_reuse",
        "title": "Double Trouble (OTP Reuse)",
        "category": "Crypto",
        "difficulty": "Medium",
        "author": "Muzammil",
        "description": "Break OTP reuse with XOR.",
        "file": "c2_otp_reuse.txt",
        "route": None,
        "flag": "DNCTF{otp_reuse_fail}"
    },

    "c3_custom_cipher": {
        "id": "c3_custom_cipher",
        "title": "Broken Shinigami Cipher",
        "category": "Crypto",
        "difficulty": "Hard",
        "author": "Muzammil",
        "description": "Break a flawed custom cipher.",
        "file": "c3_custom_cipher.txt",
        "route": None,
        "flag": "DNCTF{cipher_cracked_2047}"
    },
    
    # done
    "c4_double": {
        "id": "c4_double",
        "title": "Layers of Light",
        "category": "Crypto",
        "difficulty": "Hard",
        "author": "Muzammil",
        "description": """Light Yagami was never one to leave a simple or readable message.
        behind What you've intercepted looks like a chaotic fusion of symbols
        — dots, slashes,numbers, and strange punctuation scattered like fragments of several languages.

        Some parts feel like signals that could be tapped out or flashed.
        Others resemble patterns only machines would understand.
        A few segments appear displaced, shifted, or transformed into values far from their original form.

        Each layer masks the next, and every veil must be peeled away in the correct order.
        Only then will Light’s true message finally emerge... if you’re persistent enough.""",

        "file": "c4_double.txt",
        "route": None,
        "flag": "DNCTF{Let's_make_this_a_bit_trickier...}"
    },
    
    "c004_shaheer": {
        "id": "c004_shaheer",
        "title": "Clockwork LFSR",
        "category": "Crypto",
        "difficulty": "Hard",
        "author": "Shaheer",
        "description": "Recover the hidden flag that was embedded into the plaintext..",
        "file": "clockwork_public.zip",
        "route": None,
        "flag": "DNCTF{hard_wiener_rsa}"
    },
    
    # "upcoming": {
    #     "id": "upcoming",
    #     "title": "upcoming",
    #     "category": "Crypto",
    #     "difficulty": "Hard",
    #     "author": "Shaheer",
    #     "description": "Coming soon no file yet",
    #     # "file": "None",
    #     "route": None,
    #     "flag": "None"
    # },
    
    # ------------------- Special -------------------
    
    # done
    
    "s3": {
        "id": "s3",
        "title": "Wifi-handshake",
        "category": "Special",
        "difficulty": "Medium",
        "author": "Muzammil",
        "description": "Crack the captured wifi-handshake with popular list.",
        "file": "Capture_handshake-01.cap",
        "route": None,
        "flag": "DNCTF{FAKEWifi}"
    },
    
    "s01": {
        "id": "s01",
        "title": "Tone dialing",
        "category": "Special",
        "difficulty": "Hard",
        "author": "Muzammil",
        "description": "At 1pm I called my uncle who was 64 years old 10 months ago, but I heard only that. Later I started thinking about the 24 hour clock.\n\nHint: Instead of * use whitespaces and flag ending with } ",
        # DTMF decoder
        "file": "dial_the_number.wav",
        "route": None,
        "flag": "DNCTF{CRY}"
    },
    
    "s1": {
        "id": "s1",
        "title": "Spectrograms Waterfall",
        "category": "Special",
        "difficulty": "Hard",
        "author": "Muzammil",
        "description": "A spectrogram is a visual representation of the spectrum of frequencies of a signal as it varies with time. .",
        "file": "secretaudio_1559007588454.wav",
        "route": None,
        "flag": "DNCTF{Super_Secret_Message}"
    },
    
    # done
    "o2_shadow_request": {
    "id": "o2_shadow_request",
    "title": "Shadow Request of Kira",
    "category": "Special",
    "difficulty": "Hard",
    "author": "Muzammil",
    "description": """The server recorded something unusual—one request that shouldn’t exist.  
    Find the attacker’s IP and the exact moment they struck.

    Flag format: DNCTF{IP:Timestamp}
    Timestamp: [DD/MMM/YYYY:HH:MM:SS +XXXX]""",

    "route": None,
    "file": "shadow_access.log",
    "flag": "DNCTF{203.0.113.77:[24/Feb/2025:03:33:33 +0000]}"
    },

    
}

# ========================================================
#                    DATABASE HELPERS
# ========================================================

def get_db():
    return sqlite3.connect(DB_PATH)

def get_solved():
    solved = session.get("solved_challenges")
    return set(solved) if isinstance(solved, list) else set()

def save_solved(solved_set):
    session["solved_challenges"] = list(solved_set)


# ========================================================
#                      MAIN PAGE
# ========================================================

@app.route("/")
def index():

    solved = get_solved()

    total_easy = sum(1 for c in CHALLENGES.values() if c["difficulty"] == "Easy")
    total_medium = sum(1 for c in CHALLENGES.values() if c["difficulty"] == "Medium")
    total_hard = sum(1 for c in CHALLENGES.values() if c["difficulty"] == "Hard")

    easy_solved = sum(1 for cid in solved if CHALLENGES[cid]["difficulty"] == "Easy")
    medium_solved = sum(1 for cid in solved if CHALLENGES[cid]["difficulty"] == "Medium")
    hard_solved = sum(1 for cid in solved if CHALLENGES[cid]["difficulty"] == "Hard")

    pct = lambda d, t: int(d * 100 / t) if t else 0

    return render_template("index.html",
        challenges=CHALLENGES,
        solved=solved,
        total_easy=total_easy,
        total_medium=total_medium,
        total_hard=total_hard,
        easy_solved=easy_solved,
        medium_solved=medium_solved,
        hard_solved=hard_solved,
        easy_percent=pct(easy_solved, total_easy),
        medium_percent=pct(medium_solved, total_medium),
        hard_percent=pct(hard_solved, total_hard),
    )


# ========================================================
#                 API — CHALLENGE INFO
# ========================================================

@app.route("/api/challenge/<cid>")
def api_challenge(cid):

    ch = CHALLENGES.get(cid)
    if not ch:
        return jsonify({"error": "Unknown challenge"}), 404

    data = {
        "id": ch["id"],
        "title": ch["title"],
        "category": ch["category"],
        "difficulty": ch["difficulty"],
        "author": ch["author"],
        "description": ch["description"],
        "route": ch["route"],
        "file": ch.get("file"),
         "points": ch.get("points"), 
        "solved": cid in get_solved(),
    }

    return jsonify(data)



# ========================================================
#              FILE DOWNLOAD ROUTES
# ========================================================

@app.route("/forensics/files/<path:fname>")
def forensics_files(fname):
    return send_from_directory("challenges/forensics/files", fname, as_attachment=True)

@app.route("/osint/files/<path:fname>")
def osint_files(fname):
    return send_from_directory("challenges/osint/files", fname, as_attachment=True)

@app.route("/crypto/files/<path:fname>")
def crypto_files(fname):
    return send_from_directory("challenges/crypto/files", fname, as_attachment=True)

@app.route("/special/files/<path:fname>")
def special_files(fname):
    return send_from_directory("challenges/special/files", fname, as_attachment=True)


# ========================================================
#                 SUBMIT FLAG
# ========================================================

@app.route("/api/submit_flag", methods=["POST"])
def api_submit_flag():

    data = request.get_json(force=True)
    cid = data.get("id")
    submitted = (data.get("flag") or "").strip()

    ch = CHALLENGES.get(cid)
    if not ch:
        return jsonify({"correct": False, "message": "Unknown challenge."}), 400

    if submitted == ch["flag"]:
        solved = get_solved()
        solved.add(cid)
        save_solved(solved)
        return jsonify({"correct": True, "message": "Correct! Challenge solved."})

    return jsonify({"correct": False, "message": "Incorrect flag."})


# ========================================================
#                    RESET PROGRESS
# ========================================================

@app.route("/reset_progress")
def reset_progress():
    session["solved_challenges"] = []
    return "Progress reset! All challenges marked unsolved."



# ========================================================
#               REGISTER ALL ROUTES
# ========================================================

register_sqli_easy(app, get_db)
register_sqli_union(app, get_db)
register_blind_sqli(app, get_db)
register_xss_reflected(app, get_db)
register_xss_stored(app, get_db)
register_csrf_easy(app, get_db)
register_auth_bruteforce(app, get_db)
register_idor(app, get_db)
register_directory_fuzz(app, get_db)
register_path_traversal(app, get_db)
register_command_injection(app, get_db)
register_ssrf_basic(app, get_db)

# ========================================================
#                      RUN APP
# ========================================================

if __name__ == "__main__":
    from database.init_db import init_db
    init_db()
    app.run(debug=True)
