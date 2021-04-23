import sqlite3


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
