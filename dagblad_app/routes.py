from flask import render_template, url_for, request, redirect
from dagblad_app import app
from dagblad_app.databas import db


@app.route('/')
def index():
    hund_list = []
    db.cursor.execute("select namn, fyear from hund")
    for hund in db.cursor:
        hund_list.append(hund)
    return render_template("index.html", hund_list = hund_list)


@app.route('/edit/')
def edit():
    return render_template("new.html")

@app.route('/admin/')
def admin():
    return render_template("admin.html")

@app.route('/remove/', methods=['POST'])
def remove():
    name = request.form["article_being_removed"]
    db.cursor.execute("delete from hund where namn='{}'".format(name))
    return redirect("/")