"""
form_app.py
===========
Flask web server that serves the interactive PDF form and calls pdf_generator.

Run:
    python form_app.py
Then open:  http://localhost:5050
"""

import io
import json
import os
import tempfile
import traceback

from flask import Flask, jsonify, render_template_string, request, send_file

# Import the generator from the same directory
import sys
sys.path.insert(0, os.path.dirname(__file__))
from pdf_generator import generate_pdf

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024  # 8 MB upload limit

# ---------------------------------------------------------------------------
# Read the HTML template from a sibling file
# ---------------------------------------------------------------------------
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "form.html")


@app.route("/")
def index():
    with open(TEMPLATE_PATH, encoding="utf-8") as f:
        return render_template_string(f.read())


# ---------------------------------------------------------------------------
# /generate  — POST multipart/form-data
# ---------------------------------------------------------------------------
@app.route("/generate", methods=["POST"])
def generate():
    try:
        style = request.form.get("style", "professional").strip()

        # ---- core fields ----
        data = {}
        for field in ("title", "subtitle", "date", "reference",
                      "company", "contact", "ascii_art", "hash_id"):
            val = (request.form.get(field) or "").strip()
            if val:
                data[field] = val

        # ---- sections (JSON array sent as string) ----
        sections_raw = request.form.get("sections", "[]")
        sections = json.loads(sections_raw)
        # drop empty entries
        sections = [s for s in sections
                    if (s.get("heading") or "").strip()
                    or (s.get("body") or "").strip()]
        if sections:
            data["sections"] = sections

        # ---- table ----
        table_raw = request.form.get("table", "{}")
        table = json.loads(table_raw)
        headers = [h for h in table.get("headers", []) if str(h).strip()]
        rows    = [
            [str(c) for c in row]
            for row in table.get("rows", [])
            if any(str(c).strip() for c in row)
        ]
        if headers and rows:
            data["table"] = {"headers": headers, "rows": rows}

        # ---- logo upload (professional only) ----
        logo_file = request.files.get("logo")
        logo_tmp  = None
        if logo_file and logo_file.filename:
            suffix = os.path.splitext(logo_file.filename)[-1].lower()
            if suffix in (".png", ".jpg", ".jpeg"):
                logo_tmp = tempfile.NamedTemporaryFile(
                    suffix=suffix, delete=False
                )
                logo_file.save(logo_tmp.name)
                data["logo_path"] = logo_tmp.name

        # ---- generate into a temp file, stream back ----
        out_tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
        out_tmp.close()

        generate_pdf(style, data, out_tmp.name)

        # Build a friendly filename
        safe_title = "".join(
            c if c.isalnum() or c in "-_ " else "_"
            for c in data.get("title", "document")
        ).strip().replace(" ", "_")[:40]
        filename = f"{safe_title}_{style}.pdf"

        with open(out_tmp.name, "rb") as f:
            pdf_bytes = f.read()

        # Clean up temp files
        os.unlink(out_tmp.name)
        if logo_tmp:
            os.unlink(logo_tmp.name)

        return send_file(
            io.BytesIO(pdf_bytes),
            mimetype="application/pdf",
            as_attachment=True,
            download_name=filename,
        )

    except Exception:
        tb = traceback.format_exc()
        return jsonify({"error": tb}), 500


if __name__ == "__main__":
    print("\n  PDF Form Studio")
    print("  ───────────────")
    print("  Open in browser →  http://localhost:5050\n")
    app.run(port=5050, debug=False)
