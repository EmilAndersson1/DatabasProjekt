import psycopg2

class db():
    conn = psycopg2.connect(dbname="ak0609", user="ak0609", password="r3ayoie5", host="pgserver.mah.se")
    cursor = conn.cursor()
    