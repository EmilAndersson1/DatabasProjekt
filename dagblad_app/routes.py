from flask import render_template, url_for, request, redirect
from dagblad_app import app
from dagblad_app.databas import db


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/new/')
def new():
    return render_template("new.html")

@app.route('/admin/')
def admin():
    image_list = []
    db.cursor.execute("select image_url, alt_text from images")
    for image in db.cursor:
        image_list.append(image)
    return render_template("admin.html", image_list = image_list)

@app.route('/remove/', methods=['POST'])
def remove():
    name = request.form["article_being_removed"]
    db.cursor.execute("delete from hund where namn='{}'".format(name))
    return redirect("/")

@app.route('/new_author/')
def new_author():
    return render_template("new_author.html")

@app.route('/add_author/', methods=['POST'])
def add_author():
    author_name = request.form["author_name"]
    person_nr = request.form["person_nr"]
    notes = request.form["notes"]
    sql = """INSERT INTO author VALUES (%s, %s, %s)"""
    db.cursor.execute(sql, (person_nr, author_name, notes))
    db.conn.commit()
    return redirect(url_for("admin"))