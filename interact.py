from flask import Flask, redirect, url_for, render_template, request, session
from datetime import timedelta
import sqlite3
app = Flask(__name__)


class Element():
    def __init__(self, director, writer, cast):
        self.d = director
        self.w = writer
        self.c = cast


def query_sql(query):
    connection = sqlite3.connect("top_movie.sqlite")
    cursor = connection.cursor()
    result = cursor.execute(query).fetchall()
    connection.close()
    return result


def element_wraper(c, d, w):
    ls = []
    for i in range(len(c)):
        director = " " if i >= len(d) else d[i]
        writer = " " if i >= len(w) else w[i]
        ls.append(Element(director, writer, c[i]))
    return ls


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/movie", methods=["POST", "GET"])
def movie():
    nm = [i[0] for i in query_sql("SELECT Movie FROM movie")]
    if request.method == "POST":
        select = request.form.get('movie_name')
        if select is not None:
            select = "\""+select + "\""

            q = "select Casts from movie M join cast C ON M.MovieID=C.movieID AND M.movie={}".format(
                select)
            c = [i[0] for i in query_sql(q)]
            c = list(set(c))
            q = "select Directors from movie M join director D ON M.MovieID=D.movieID AND M.movie={}".format(
                select)
            d = [i[0] for i in query_sql(q)]
            d = list(set(d))
            q = "select Writers from movie M join writer W ON M.MovieID=W.movieID AND M.movie={}".format(
                select)
            w = [i[0] for i in query_sql(q)]
            w = list(set(w))

            e = element_wraper(c, d, w)
            return render_template(
                "movie.html", element=e, name=nm,
                table=True)

    return render_template("movie.html", name=nm, table=False)


if __name__ == "__main__":

    app.run(debug=True)
