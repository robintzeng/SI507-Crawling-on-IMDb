import sqlite3
import datetime

connection = sqlite3.connect("top_movie.sqlite")
cursor = connection.cursor()
name = "\"The Shawshank Redemption_1994\""
query = "Select Date, Star From movie order by Date"
print(query)

result = cursor.execute(query).fetchall()
print(result[0][0].split()[0])
print(datetime.datetime.strptime(result[0][0].split()[0], '%Y-%m-%d'))
# d = {}

# for i in result:
#     print(i)
#     if i[0] not in d:
#         print(i[0])
#         print(i[1])
#         d[i[0]] = [0, 0]
#         d[i[0]][0] = 1
#         d[i[0]][1] = i[1]
#     else:
#         d[i[0]][0] = d[i[0]][0] + 1
#         d[i[0]][1] = d[i[0]][1] + i[1]

# x = d.keys()
# print(d)
# # for key in d.keys():
# y = [d[key][1]/d[key][0] for key in d.keys()]

# print(list(x))
# print(y)

#x = [i[0] for i in result]
# print(result)
connection.close()
