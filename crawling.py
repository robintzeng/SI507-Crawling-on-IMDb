import requests
from bs4 import BeautifulSoup
import pandas as pd
base_url = "https://www.imdb.com"
full_cast_url = "fullcredits?ref_=tt_cl_sm#cast"
url = base_url + "/chart/top/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
result = soup.find_all("td", class_="titleColumn")
print(result[0].select('a')[0].getText())  # movie name
print(result[0].find_all(href=True)[0]['href'])  # movie link

movie_link = result[0].find_all(href=True)[0]['href']

url_craw = base_url + movie_link
# print(url_craw)
response_craw = requests.get(url_craw)
soup_craw = BeautifulSoup(response_craw.text, "html.parser")
mydivs = soup_craw.find_all("div", class_="credit_summary_item")
'''
print("Director")
for director in mydivs[0].select('a'):  # Director
    print(director.getText())
print("\n")
print("Writer")
for writer in mydivs[1].select('a'):  # Writer
    print(writer.getText())
print("\n")

mydivs = soup_craw.find_all("div", class_="article", id="titleCast")
print("CASTS")
for cast in mydivs[0].find_all('td', class_='primary_photo'):  # casts
    print(cast.find('img').get('alt'))
print("\n")

# Box info
print("BOX")
mydivs = soup_craw.find_all("div", class_="article", id="titleDetails")
print(mydivs[0].find_all("div", class_="txt-block")  # country
      [1].find_all("a")[0].getText())

print(mydivs[0].find_all("div", class_="txt-block")  # language
      [2].find_all("a")[0].getText())

print(mydivs[0].find_all("div", class_="txt-block")  # date
      [3].find("h4").next_sibling)

print(mydivs[0].find_all("div", class_="txt-block")  # budget
      [6].find_all("h4")[0].next_sibling)

print(mydivs[0].find_all("div", class_="txt-block")  # gross USA
      [8].find_all("h4")[0].next_sibling)

print(mydivs[0].find_all("div", class_="txt-block")  # cumulative worldwide
      [9].find_all("h4")[0].next_sibling)
'''
mydivs = soup_craw.find_all("div", class_="title_bar_wrapper")
print(mydivs[0].find_all("div", class_="subtext")  # genre
      [0].find("a").getText())
