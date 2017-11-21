import requests
import pymongo
from pyquery import PyQuery as pq
from selenium import webdriver

client = pymongo.MongoClient()
db = client.nuomi
col_citycode = db.citycode
col_movieid = db.movieid
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'
}
cityname = '广州'
data = col_citycode.find({'cityname': cityname})
citycode = data[0]['citycode']
print(citycode)

url = 'https://mdianying.baidu.com/?page=movie&cc={}'.format(citycode)
# path = r"C:\phantomjs\bin\phantomjs.exe"
path = r"C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chrome.exe"

browser = webdriver.Chrome()
browser.set_window_size(1366, 768)
browser.get(url)
html = browser.page_source
doc = pq(html)
movies = doc('.movie-detail-link')
print(len(movies))
for i in range(len(movies)):
    movie = movies.eq(i)
    movie_name = movie.find('.movie-name-text').text()
    movie_id = movie.find('.poster-show').attr('data-movieid')
    print(movie_name, movie_id)
    try:
        print('collect', movie_name)
        col_movieid.update({'movie_id': movie_id}, {'$set': {'movie_id': movie_id, 'movie_name': movie_name}},
                           upsert=True)
        print('saved')
    except Exception as e:
        print(e)
