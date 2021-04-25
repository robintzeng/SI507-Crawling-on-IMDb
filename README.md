# Scraping-on-IMDb


# Data Proparation
**crawling.py:** the function will scrape the chart from [IMDB](https://www.imdb.com/chart/top/), and crawl the data like box, casts, directors...  <br>
Also, we use caching, thus the cache cache data will be solved into cache_data

**json2sql.py:** the function will turn the raw data we scrape online into sql database. 

# Installation: 

### conda environment setting
```
conda env create -f environment.yml -n si507
```
### Start conda environment
```
conda activate si507
```