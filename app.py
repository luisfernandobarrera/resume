import jinja2
from flask import Flask, render_template, Response, jsonify, url_for
import json
import sass
import os
import glob
import logging

logger = logging.getLogger(__name__)

try:
    from flask_weasyprint import HTML, render_pdf
    PDF_SUPPORT = True
    logging.info(f"* PDF support enabled")

except (ImportError, OSError):
    PDF_SUPPORT = False
    logging.info(f"* PDF support disabled")


app = Flask(__name__)
files = glob.glob("*.resume.json")
if files:
    RESUME = files[0]
else:
    assert False, "Cannot load resume.json"


@app.route("/")
def cv():
    with open(RESUME, encoding="utf-8") as o:
        document = json.load(o)
    return render_template("template.html", resume=document)


@app.route("/resume.json")
def resume():
    with open(RESUME, encoding="utf-8") as o:
        return jsonify(json.load(o))


@app.route("/style.css")
def style():
    with open("templates/sass/style.sass") as r:
        css = sass.compile(string=r.read(), indented=True)
    return Response(css, mimetype="text/css")


# PDF Support
if PDF_SUPPORT:
    @app.route('/cv.pdf')
    def cv_pdf():
        return render_pdf(url_for('cv'))


# For Github Pages
with open(RESUME, encoding="utf-8") as o:
    document = json.load(o)
gh_pages = document.get('meta', {}).get('gh-pages-domain') or None
if gh_pages:
    @app.route("/CNAME")
    def cname():
        return Response(gh_pages, mimetype="application/octet-stream")


