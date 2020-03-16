from flask import render_template, url_for, request, redirect
from dagblad_app import app
from dagblad_app.databas import db
from datetime import datetime


@app.route('/')
def index():
    article_list = []
    db.cursor.execute("select headline, preamble, published from article")
    for article in db.cursor:
        article_list.append(article)
    
    return render_template("index.html", article_list = article_list)


@app.route('/new_article/')
def new_article():
    author_list = []
    db.cursor.execute("select author_name, person_nr, notes from author")
    for author in db.cursor:
        author_list.append(author)
    return render_template("new.html", author_list = author_list)

@app.route('/add_article/', methods=['POST'])
def add_article():
    now = datetime.now()

    author_personnummer = request.form["author_personnummer"]
    headline = request.form["headline"]
    preamble = request.form["article_preamble"]
    article_text = request.form["article_text"]
    time_published = now.strftime("%Y-%m-%d %H:%M")

    sql = "INSERT INTO article VALUES (DEFAULT,%s, %s, %s, %s)"
    db.cursor.execute(sql, (headline, preamble, article_text, time_published))
    
    sql = "INSERT INTO article_author VALUES (DEFAULT, %s)" 
    db.cursor.execute(sql, (author_personnummer,))

    db.conn.commit()

    return redirect(url_for("admin"))

@app.route('/remove_article/', methods=['POST'])
def remove_article():
    article_being_removed = request.form["article_being_removed"]

    sql = "delete from article_author where article_id = %s"
    db.cursor.execute(sql,(article_being_removed,))

    sql = "delete from article where article_id = %s"
    db.cursor.execute(sql,(article_being_removed,))

    db.conn.commit()

    return redirect(url_for("admin"))

@app.route('/admin/')
def admin():
    author_list = []
    db.cursor.execute("select author_name, person_nr, notes from author")
    for author in db.cursor:
        author_list.append(author)

    article_list = []
    db.cursor.execute("select article.article_ID, article.headline, article.preamble, article.published, author.author_name \
                        from article \
                        inner join article_author \
                            ON article.article_id=article_author.article_id \
                        inner join author \
                            ON author.person_nr=article_author.person_nr")
    for article in db.cursor:
        article_list.append(article)

    return render_template("admin.html", author_list = author_list, article_list = article_list)


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