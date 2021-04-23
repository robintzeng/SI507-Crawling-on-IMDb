import sqlite3
connection = sqlite3.connect("top_movie.sqlite")
cursor = connection.cursor()
name = "\"The Shawshank Redemption_1994\""
query = "select Casts from movie M join cast C ON M.MovieID=C.movieID AND M.movie={}".format(
    name)

result = cursor.execute(query).fetchall()
x = [i[0] for i in result]
print(x)
connection.close()
