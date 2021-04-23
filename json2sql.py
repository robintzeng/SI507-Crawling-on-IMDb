import json
import locale
import sqlite3
from datetime import datetime


def create_table(conn):
    cur = conn.cursor()

    create_movie = '''
    CREATE TABLE IF NOT EXISTS "movie" (
        "ID"        INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        "Movie"     TEXT NOT NULL,
        "MovieID"   INTEGER,
        "Genre"     TEXT NOT NULL,
        "Country"   TEXT NOT NULL,
        "Star"      FLOAT NOT NULL,
        "Language"  TEXT NOT NULL,
        "Date"      DATE NOT NULL,
        "Budget"    FLOAT,
        "USA_Gross" FLOAT,
        "World_Gross" FLOAT
        );
    '''
    create_cast = '''
    CREATE TABLE IF NOT EXISTS "cast" (
        "ID"        INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        "Casts"      TEXT NOT NULL,
        "MovieID"     INTEGER,
        FOREIGN KEY (MovieID) REFERENCES movie(MovieID)
        );
    '''
    create_director = '''
    CREATE TABLE IF NOT EXISTS "director" (
        "ID"        INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        "Directors"      TEXT NOT NULL,
        "MovieID"     INTEGER,
        FOREIGN KEY (MovieID) REFERENCES movie(MovieID)
        );
    '''
    create_writer = '''
    CREATE TABLE IF NOT EXISTS "writer" (
        "ID"        INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        "Writers"      TEXT NOT NULL,
        "MovieID"     INTEGER,
        FOREIGN KEY (MovieID) REFERENCES movie(MovieID)
        );
    '''
    cur.execute(create_movie)
    cur.execute(create_cast)
    cur.execute(create_director)
    cur.execute(create_writer)
    conn.commit()


def money_exchange(money):
    if money == 0:
        return 0
    if money[0] == '$':
        return locale.atof(money.strip('$'))
    currency = money[0:3]
    money = money[3:]
    if currency == "TRL":
        return locale.atof(money)*0.1239
    elif currency == "RUR":
        return locale.atof(money)*0.01318
    elif currency == "KRW":
        return locale.atof(money)*0.000896
    elif currency == "JPY":
        return locale.atof(money)*0.009192
    elif currency == "INR":
        return locale.atof(money)*0.013416
    elif currency == "GBP":
        return locale.atof(money)*1.383349
    elif currency == "FRF":
        return locale.atof(money)*0.182662
    elif currency == "EUR":
        return locale.atof(money)*1.198194
    elif currency == "DEM":
        return locale.atof(money)*0.61258
    elif currency == "BRL":
        return locale.atof(money)*0.178978
    elif currency == "AUD":
        return locale.atof(money)*0.7734


def insert_data(data, conn):
    for i, key in enumerate(data.keys()):
        print(key, i)
        d = data[key]
        cur = conn.cursor()

        insert_movies = '''
        INSERT INTO movie
        VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)
        '''
        name = d['name']
        country = d['country']
        star = float(d['star'])
        language = d['language']
        genre = d['genre']
        try:
            dt = datetime.strptime(d['date'], '%d %B %Y')
        except:
            d['date'] = "15 " + d['date']
            dt = datetime.strptime(d['date'], '%d %B %Y')
        budget = money_exchange(d['box']['budget'])
        us = money_exchange(d['box']['usa'])
        world = money_exchange(d['box']['world'])
        movie_ls = [name, i+1, genre, country, star,
                    language, dt, budget, us, world]
        cur.execute(insert_movies, movie_ls)
        conn.commit()

        for director in d['directors']:
            insert_director = '''
            INSERT INTO director
            VALUES (NULL, ?, ?)
            '''
            director_ls = [director, i+1]
            cur.execute(insert_director, director_ls)
            conn.commit()

        for writer in d['writers']:
            insert_writer = '''
            INSERT INTO writer
            VALUES (NULL, ?, ?)
            '''
            writer_ls = [writer, i+1]
            cur.execute(insert_writer, writer_ls)
            conn.commit()

        for cast in d['casts']:
            insert_cast = '''
            INSERT INTO cast
            VALUES (NULL,?, ?)
            '''
            cast_ls = [cast, i+1]
            cur.execute(insert_cast, cast_ls)
            conn.commit()


if __name__ == "__main__":
    conn = sqlite3.connect("top_movie.sqlite")
    locale.setlocale(locale.LC_ALL, 'en_US.UTF8')
    create_table(conn)
    with open('cache_data/movie_info_cache.json') as f:
        data = json.load(f)
    insert_data(data, conn)
