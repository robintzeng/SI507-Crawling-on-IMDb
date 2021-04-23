from flask import Flask, redirect, url_for, render_template, request, session
from datetime import timedelta, datetime
import plotly.graph_objs as go
from helper import *
import sqlite3

rating_select = None

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
            print("DDD")
            # return redirect(url_for('movie', element=e, name=nm,
            #                         table=True))
            return render_template(
                "movie.html", element=e, name=nm,
                table=True)

    return render_template("movie.html", name=nm, table=False)


@app.route("/rating", methods=["POST", "GET"])
def rating():
    global rating_select
    if request.method == "POST":
        print("METHOD")
        select = request.form.get('rating_name')
        if select is not None or rating_select is not None:
            if select is not None:
                rating_select = select
            if rating_select == "table":
                q = "select movie, Star, Date from movie M"
                ret = query_sql(q)
                movie_name = [i[0] for i in ret]
                star = [i[1] for i in ret]
                date = [i[2].split()[0] for i in ret]
                e = element_wraper(movie_name, star, date)
                return render_template(
                    "rating.html", element=e, type="table", show=True)
            elif rating_select == "star":
                if request.method == "POST":
                    chart = request.form.get('chart_type')
                    q = "select Genre , Star from movie M "
                    result = query_sql(q)
                    d = {}
                    for i in result:
                        if i[0] not in d:
                            d[i[0]] = [0, 0]
                            d[i[0]][0] = 1
                            d[i[0]][1] = i[1]
                        else:
                            d[i[0]][0] = d[i[0]][0] + 1
                            d[i[0]][1] = d[i[0]][1] + i[1]

                    f = go.Bar
                    print(chart)
                    if chart == "pie":
                        f = go.Pie
                    x = list(d.keys())
                    y = [d[key][0] for key in d.keys()]

                    plt = create_plot(x, y, func=f)
                    return render_template(
                        "rating.html", type="star", plot=plt, show=True)

            elif rating_select == "time":
                if request.method == "POST":
                    chart = request.form.get('chart_type')
                    q = "Select Date, Star From movie order by Date"
                    result = query_sql(q)

                    x = [datetime.strptime(x[0].split()[0], '%Y-%m-%d')
                         for x in result]
                    y = [float(x[1]) for x in result]
                    f = go.Scatter
                    if chart == 'line':
                        f = go.Line
                    plt = create_plot(x, y, func=f)
                    return render_template(
                        "rating.html", type="time", plot=plt, show=True)

    return render_template("rating.html", show=False)


if __name__ == "__main__":
    app.run(debug=True)
