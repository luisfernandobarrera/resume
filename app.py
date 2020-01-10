import jinja2
from flask import Flask, render_template, Response, jsonify
import json
import sass
import os
import glob

app = Flask(__name__)
files = glob.glob("*.resume.json")
if files:
    RESUME = files[0]

assert RESUME, "Cannot load resume.json"


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

