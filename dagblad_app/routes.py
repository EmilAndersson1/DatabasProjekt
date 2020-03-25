from flask import render_template, url_for, request, redirect
from dagblad_app import app
from dagblad_app.databas import db
from datetime import datetime


@app.route('/')
def index():
    article_list = []
    db.cursor.execute("select headline, preamble, published, article_id from article order by published DESC")
    for article in db.cursor:
        article_list.append(article)
    
    return render_template("index.html", article_list = article_list)

@app.route('/add-image/')
def add_image():
    return render_template("add-image.html")

@app.route('/add_image_to_db/', methods=['POST'])
def add_image_to_db():
    url = request.form["url"]
    alt_text = request.form["alt_text"]

    sql = "insert into images values (%s,%s)"
    db.cursor.execute(sql, (url,alt_text))
    db.conn.commit()
    return redirect(url_for("new_article"))


@app.route('/dagblad/<article_id>/')
def show_dagblad(article_id):
    article = []
    sql = "select article_id, headline, preamble, article_text, published from article where article_id = %s"
    db.cursor.execute(sql,(article_id,))

    [article.append(a) for articles in db.cursor for a in articles ]

    author = []
    sql2 = "select author.author_name \
            from author \
            inner join article_author\
                on author.person_nr=article_author.person_nr\
            where article_author.article_id = %s"      
    db.cursor.execute(sql2,(article_id,))
    [author.append(a) for authors in db.cursor for a in authors ]

    commenter = []
    sql3 = "select commenter.username, commenter.comment, commenter.curr_time, commenter.commenter_ID, commenter.article_ID \
            from commenter join article \
                on article.article_id = commenter.article_id \
            where article.article_id = %s order by commenter.curr_time DESC"    
    db.cursor.execute(sql3,(article_id,))
    for comment in db.cursor:
        commenter.append(comment)

    image_list = []
    sql4 = "select images.image_url, images.alt_text, images_in_article.image_text \
            from images \
            join images_in_article \
                on images.image_url = images_in_article.image_url \
            where images_in_article.article_id = %s"

    db.cursor.execute(sql4,(article_id,))
    [image_list.append(images) for images in db.cursor]
    
    return render_template("dagblad.html", article = article, authors = author, image_list=image_list, commenter=commenter)


@app.route('/new_article/')
def new_article():
    author_list = []
    db.cursor.execute("select author_name, person_nr, notes from author")
    for author in db.cursor:
        author_list.append(author)
    
    image_list = []
    db.cursor.execute("select * from images")
    for image in db.cursor:
        image_list.append(image)
    return render_template("new.html", author_list = author_list, image_list = image_list)

@app.route('/add_article/', methods=['POST'])
def add_article():
    now = datetime.now()
    author_personnummer = []
    author_personnummer = request.form.getlist("author_personnummer")
    headline = request.form["headline"]
    preamble = request.form["article_preamble"]
    article_text = request.form["article_text"]
    time_published = now.strftime("%Y-%m-%d %H:%M")

    url = request.form.getlist("url")
    image_text = request.form.getlist("image_text")

    for text in image_text:
        if text == "":
            image_text.remove(text)

    sql = "INSERT INTO article VALUES (DEFAULT, %s, %s, %s, %s)"
    db.cursor.execute(sql, (headline, preamble, article_text, time_published))
    
    for author in author_personnummer:
        sql = "INSERT INTO article_author(article_id, person_nr) select article_id, %s from article where preamble = %s and headline = %s and published = %s and article_text = %s"
        db.cursor.execute(sql,(author, preamble, headline, time_published, article_text))
    index = 0
    for url in url:
        sql = "insert into images_in_article(image_url,article_id,image_text) select %s, article_id, %s from article where preamble = %s and headline = %s and published = %s and article_text = %s"
        db.cursor.execute(sql,(url, image_text[index], preamble, headline, time_published, article_text))
        index =+ 1
    
    db.conn.commit()

    return redirect(url_for("admin"))

@app.route('/remove_article/', methods=['POST'])
def remove_article():
    article_being_removed = request.form["article_being_removed"]

    sql = "delete from commenter where article_id = %s"
    db.cursor.execute(sql,(article_being_removed,))

    sql = "delete from images_in_article where article_id = %s"
    db.cursor.execute(sql,(article_being_removed,))

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
    db.cursor.execute("select article.article_ID, article.headline, article.preamble, article.published from article")     
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

@app.route('/add_comment/', methods=['POST'])
def add_comment():
    article_ID = request.form["article_ID"]
    username = request.form["username"]
    comment = request.form["comment"]
    now = datetime.now()
    time_published = now.strftime("%Y-%m-%d %H:%M")

    
    sql = "INSERT INTO commenter VALUES (DEFAULT, %s, %s, %s, %s)"
    db.cursor.execute(sql, (article_ID, username, comment, time_published))
    db.conn.commit()

    return redirect("/dagblad/{}/".format(article_ID))

@app.route('/remove_comment/', methods=['POST'])
def remove_comment():
    comment_being_removed = request.form["comment_being_removed"]
    article_ID = request.form["comment_being_removed_ID"]

    sql = "delete from commenter where commenter_ID = %s"
    db.cursor.execute(sql,(comment_being_removed,))
    db.conn.commit()

    return redirect("/dagblad/{}/".format(article_ID))
