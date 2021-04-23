from flask import Flask, redirect, url_for, render_template, request, session
from datetime import timedelta
from helper import *
import sqlite3
app = Flask(__name__)


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


@app.route("/rating", methods=["POST", "GET"])
def rating():
    if request.method == "POST":
        select = request.form.get('rating_name')
        if select is not None:
            q = "select movie, Star, Date from movie M"
            ret = query_sql(q)
            movie_name = [i[0] for i in ret]
            star = [i[1] for i in ret]
            date = [i[2].split()[0] for i in ret]
            e = element_wraper(movie_name, star, date)
            return render_template(
                "rating.html", element=e, type="table", show=True)

    return render_template("rating.html", show=False)


if __name__ == "__main__":
    app.run(debug=True)
