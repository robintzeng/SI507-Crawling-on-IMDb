import sqlite3
connection = sqlite3.connect("top_movie.sqlite")
cursor = connection.cursor()
name = "\"The Shawshank Redemption_1994\""
query = "select movie , Star,Date  from movie M"

result = cursor.execute(query).fetchall()
x = [i[0] for i in result]
print(result)
connection.close()
