import jinja2
from flask import Flask, render_template, Response, jsonify, url_for, make_response
import json
import sass
import os
import glob
import logging

os.environ['LC_ALL'] = 'en_US.utf-8'

logger = logging.getLogger(__name__)

try:
    from flask_weasyprint import HTML, render_pdf

    PDF_SUPPORT = True
    logging.info("* PDF support enabled")

except (ImportError, OSError):
    PDF_SUPPORT = False
    logging.info("* PDF support disabled")

app = Flask(__name__, template_folder="templates")

if files := glob.glob("*.resume.json"):
    RESUME = files[0]
else:
    assert False, "Cannot load resume.json"


if files := glob.glob("resume.pdf"):
    RESUME_PDF = files[0]
else:
    assert False, "Cannot load resume.pdf"


@app.route("/")
def cv():
    with open(RESUME, encoding="utf-8") as o:
        document = json.load(o)
    return render_template("cv_screen.html", resume=document, print=False)

# ATS HTML preview removed - only PDF version available at /resume-ats.pdf
# @app.route("/resume/")
# def resume():
#     with open(RESUME, encoding="utf-8") as o:
#         document = json.load(o)
#     return render_template("resume_ats.html", resume=document, print=False)


@app.route("/print-cv.html")
def print_cv():
    with open(RESUME, encoding="utf-8") as o:
        document = json.load(o)
    # Use original cv.html template with print CSS for PDF generation
    return render_template("cv.html", resume=document, print=True)

@app.route("/print-resume.html")
def print_resume():
    with open(RESUME, encoding="utf-8") as o:
        document = json.load(o)
    return render_template("resume_ats.html", resume=document, print=True)

@app.route("/print-resume-projects.html")
def print_resume_projects():
    with open(RESUME, encoding="utf-8") as o:
        document = json.load(o)
    return render_template("resume_with_projects.html", resume=document, print=True)


@app.route("/resume.json")
def resume_json():
    with open(RESUME, encoding="utf-8") as o:
        return jsonify(json.load(o))


@app.route("/style.css")
def style():
    # Legacy route - serves screen CSS
    return style_screen()

@app.route("/style-screen.css")
def style_screen():
    with open("templates/sass/style-screen.sass") as r:
        css = sass.compile(
            string=r.read(),
            indented=True,
            include_paths=["templates/sass"]
        )
    return Response(css, mimetype="text/css")

@app.route("/style-print.css")
def style_print():
    with open("templates/sass/style-print.sass") as r:
        css = sass.compile(
            string=r.read(),
            indented=True,
            include_paths=["templates/sass"]
        )
    return Response(css, mimetype="text/css")



# PDF Support
if PDF_SUPPORT:
    @app.route('/cv.pdf')
    def cv_pdf():
        return render_pdf(url_for('print_cv'))

    @app.route('/resume-ats.pdf')
    def resume_ats_pdf():
        return render_pdf(url_for('print_resume'))
    
    @app.route('/resume-projects.pdf')
    def resume_projects_pdf():
        return render_pdf(url_for('print_resume_projects'))


if PDF_SUPPORT:
    @app.route('/resume.pdf')
    def resume_pdf():
        # Alias for resume-ats.pdf (1-page ATS resume)
        return render_pdf(url_for('print_resume'))
else:
    @app.route('/resume.pdf')
    def resume_pdf():
        # Fallback to file if PDF generation not available
        with open(RESUME_PDF, "rb") as resume_pdf_file:
            binary_pdf = resume_pdf_file.read()
        response = make_response(binary_pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=resume.pdf'
        return response

# For GitHub Pages
with open(RESUME, encoding="utf-8") as o:
    document = json.load(o)
gh_pages = document.get('meta', {}).get('gh-pages-domain') or None
if gh_pages:
    @app.route("/CNAME")
    def cname():
        return Response(gh_pages, mimetype="application/octet-stream")
