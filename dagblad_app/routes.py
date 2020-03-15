from flask import render_template, url_for, request, redirect
from dagblad_app import app
from dagblad_app.databas import db


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/new_article/')
def new_article():
    author_list = []
    db.cursor.execute("select author_name, person_nr, notes from author")
    for author in db.cursor:
        author_list.append(author)
    return render_template("new.html", author_list = author_list)

@app.route('/add_article/', methods=['POST'])
def add_article():
    author_personnummer = request.form["author_personnummer"]
    headline = request.form["headline"]
    preamble = request.form["article_preamble"]
    article_text = request.form["article_text"]

    sql = "INSERT INTO article VALUES (DEFAULT,%s, %s, %s)"
    #default=serial
    db.cursor.execute(sql, (headline, preamble, article_text))
    

    sql = "INSERT INTO article_author VALUES (DEFAULT, %s)" 
    #default betyder att det läggs till enligt SERIAL datan
    db.cursor.execute(sql, (author_personnummer,))
    db.conn.commit()

    return redirect(url_for("admin"))

@app.route('/admin/')
def admin():
    author_list = []
    db.cursor.execute("select author_name, person_nr, notes from author")
    for author in db.cursor:
        author_list.append(author)
    return render_template("admin.html", author_list = author_list)


@app.route('/new_author/')
def new_author():
    return render_template("new_author.html")

@app.route('/add_author/', methods=['POST'])
def add_author():
    author_name = request.form["author_name"]
    person_nr = request.form["person_nr"]
    notes = request.form["notes"]
    
    sql = "INSERT INTO author VALUES (%s, %s, %s)"
    db.cursor.execute(sql, (person_nr, author_name, notes))
    db.conn.commit()
    
    return redirect(url_for("admin"))

@app.route('/remove_author/', methods=['POST'])
def remove_author():
    author_being_removed = request.form["author_being_removed"]

    sql = "delete from author where person_nr = %s"
    db.cursor.execute(sql,(author_being_removed,))
    db.conn.commit()

    return redirect(url_for("admin"))