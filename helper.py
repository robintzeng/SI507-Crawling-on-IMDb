import plotly.graph_objs as go
import sqlite3
import plotly
import pandas as pd
import json
from datetime import datetime

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


def create_plot(x, y, func):
    df = pd.DataFrame({'x': x, 'y': y})  # creating a sample dataframe

    if func == go.Pie:
        data = [
            func(
                labels=df['x'],  # assign x as the dataframe column 'x'
                values=df['y']
            )
        ]
    elif func == go.Bar:
        data = [
            func(
                x=df['x'],  # assign x as the dataframe column 'x'
                y=df['y']
            )
        ]
    elif func == go.Scatter or go.Line:
        data = [
            func(
                x=df['x'],  # assign x as the dataframe column 'x'
                y=df['y'],
                mode='markers' if func == go.Scatter else None
            )
        ]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

def calculate_money_date(date, money):
    d = datetime(1921,1,1,0,0,0,0)
    ls_acc = [0]*11
    ls_num = [0]*11
    for i in range(len(date)):
        if money[i] == 0:
            continue
        else:
            tmp = datetime.strptime(date[i].split()[0], '%Y-%m-%d')
            idx = int((tmp - d).days/3650)
            ls_acc[idx] += money[i]
            ls_num[idx] += 1

    for i in range(len(ls_acc)):
        if ls_num[i] == 0:
            continue
        else:
            ls_acc[i] = ls_acc[i] / ls_num[i]
    return ls_acc
        
        

