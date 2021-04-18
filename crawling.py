import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

MOVIE_CACHE_FILENAME = "cache_data/movie_cache.json"
MOVIE_INFO_CACHE_FILENAME = "cache_data/movie_info_cache.json"
MOVIE_URL_DICT = {}
MOVIE_INFO_DICT = {}


class Box:
    def __init__(self, budget, usa, world):
        self.budget = budget
        self.usa = usa
        self.world = world


class Movie:
    def __init__(
            self, name, genre, directors, writers, casts, star, country,
            language, date, box):
        self.name = name
        self.genre = genre
        self.directors = directors
        self.writers = writers
        self.casts = casts
        self.star = star
        self.country = country
        self.language = language
        self.date = date
        self.box = box


def get_movie_url_dict():
    ''' Make a dictionary that maps state name to state page url from "https://www.nps.gov"

    Parameters
    ----------
    None

    Returns
    -------
    dict
        key is a state name and value is the url
        e.g. {'michigan':'https://www.nps.gov/state/mi/index.htm', ...}
    '''
    global MOVIE_URL_DICT
    if not MOVIE_URL_DICT:
        print("Fetching Movies!")
        movie_name_dict = {}
        url = base_url + "/chart/top/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        result = soup.find_all("td", class_="titleColumn")
        for i in range(len(result)):
            movie_name = result[i].select('a')[0].getText()  # movie name
            movie_link = result[i].find_all(href=True)[0]['href']  # movie link
            movie_year = result[i].select('span')[0].getText()[1:-1]
            movie_name_year = movie_name + '_' + movie_year
            movie_name_dict[movie_name_year] = movie_link

        MOVIE_URL_DICT = movie_name_dict
        save_cache(MOVIE_URL_DICT, MOVIE_CACHE_FILENAME)
        return MOVIE_URL_DICT
    else:
        print("Using cache!")
        return MOVIE_URL_DICT


def get_movie_info(movie_name_year):
    '''Make a list of national site instances from a state URL.

    Parameters
    ----------
    state_url: string
        The URL for a state page in nps.gov

    Returns
    -------
    list
        a list of national site instances
    '''

    if movie_name_year in MOVIE_INFO_DICT.keys():
        print("Using cache")
        return MOVIE_INFO_DICT[movie_name_year]
    else:
        print("Fetching Movie Info!")
        movie_url = MOVIE_URL_DICT[movie_name_year]
        url_craw = base_url + movie_url
        response_craw = requests.get(url_craw)
        soup_craw = BeautifulSoup(response_craw.text, "html.parser")

        star = soup_craw.find_all("span", itemprop="ratingValue")[0].getText()
        # print(star)

        mydivs = soup_craw.find_all("div", class_="credit_summary_item")
        directors = [director.getText()
                     for director in mydivs[0].select('a')]  # Director
        # print(directors)
        writers = [writer.getText()
                   for writer in mydivs[1].select('a')]  # Writer
        # print(writers)
        mydivs = soup_craw.find_all("div", class_="article", id="titleCast")
        casts = [
            cast.find('img').get('alt')
            for cast in mydivs[0].find_all('td', class_='primary_photo')]
        # print(casts)

        country = ""
        language = ""
        date = ""
        budget = 0
        usa = 0
        world = 0

        mydivs = soup_craw.find_all("div", class_="article", id="titleDetails")
        text_block = mydivs[0].find_all("div", class_="txt-block")

        for i in range(len(text_block)):
            try:
                txt = text_block[i].find_all("h4")[0].getText()[:-1]
                # print(txt)
                if txt == "Country":
                    country = text_block[i].find_all("a")[0].getText()
                    # print(country)
                elif txt == "Language":
                    language = text_block[i].find_all("a")[0].getText()
                    # print(language)
                elif txt == "Release Date":
                    date = text_block[i].find("h4").next_sibling
                    stop = date.find("(")
                    date = date[:stop].strip()

                elif txt == "Budget":
                    budget = text_block[i].find_all(
                        "h4")[0].next_sibling.strip()
                    # print(budget)
                elif txt == "Gross USA":
                    usa = text_block[i].find_all("h4")[0].next_sibling.strip()
                    # print(usa)
                elif txt == "Cumulative Worldwide Gross":
                    world = text_block[i].find_all(
                        "h4")[0].next_sibling.strip()
                    # print(world)
            except:
                pass

        mydivs = soup_craw.find_all("div", class_="title_bar_wrapper")
        genre = mydivs[0].find_all("div", class_="subtext")[
            0].find("a").getText()  # genre
        # print(genre)
        # print(usa)
        box = Box(budget, usa, world)
        movie = Movie(movie_name_year, genre, directors, writers,
                      casts, star, country, language, date, box)

        MOVIE_INFO_DICT[movie_name_year] = movie.__dict__
        save_cache(MOVIE_INFO_DICT, MOVIE_INFO_CACHE_FILENAME)
        return MOVIE_INFO_DICT


def open_cache(cache_filename):
    ''' Opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary

    Parameters
    ----------
    None

    Returns
    -------
    The opened cache: dict
    '''
    try:
        cache_file = open(cache_filename, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict


def save_cache(cache_dict, filename):
    ''' Saves the current state of the cache to disk

    Parameters
    ----------
    cache_dict: dict
        The dictionary to save

    Returns
    -------
    None
    '''

    dumped_json_cache = json.dumps(
        cache_dict, default=lambda o: o.__dict__)
    fw = open(filename, "w")
    fw.write(dumped_json_cache)
    fw.close()


if __name__ == "__main__":
    MOVIE_URL_DICT = open_cache(MOVIE_CACHE_FILENAME)
    MOVIE_INFO_DICT = open_cache(MOVIE_INFO_CACHE_FILENAME)

    base_url = "https://www.imdb.com"
    full_cast_url = "fullcredits?ref_=tt_cl_sm#cast"
    url = base_url + "/chart/top/"

    movie_name_dict = get_movie_url_dict()
    for i, key in enumerate(MOVIE_URL_DICT.keys()):
        print(i, key)
        get_movie_info(key)
