import time

import requests
import pymongo
from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def get_index():
    client = pymongo.MongoClient()
    db = client.nuomi
    col_citycode = db.citycode
    col_movieid = db.movieid

    cityname = '广州'
    movie_name = '一路绽放'
    date = '2017-11-21'

    timeArray = time.strptime(date, "%Y-%m-%d")
    timestamp = int(time.mktime(timeArray))
    print(timestamp)

    data = col_citycode.find({'cityname': cityname})
    citycode = data[0]['citycode']
    print(citycode)

    data = col_movieid.find({'movie_name': movie_name})
    movie_id = data[0]['movie_id']
    print(movie_id)
    url = 'https://mdianying.baidu.com/movie/schedule?movieId={}&sfrom=wise_shoubai&from=webapp&c={}'.format(
        movie_id, citycode)
    # path = r"C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chrome.exe"
    # chrome_options = webdriver.ChromeOptions()
    # prefs = {"profile.managed_default_content_settings.images":2}
    # chrome_options.add_experimental_option("prefs",prefs)
    # browser = webdriver.Chrome(chrome_options=chrome_options)


    path = r"C:\phantomjs\bin\phantomjs.exe"
    service_args = []
    service_args.append('--load-images=no')  ##关闭图片加载
    # service_args.append('--disk-cache=yes')  ##开启缓存
    # service_args.append('--ignore-ssl-errors=true')  ##忽略https错误

    browser = webdriver.PhantomJS(path, service_args=service_args)
    browser.set_window_size(1600, 600)
    wait = WebDriverWait(browser, 10)
    browser.get(url)

    js = "var q=document.documentElement.scrollTop=100000"
    for i in range(2):
        browser.execute_script(js)
        time.sleep(1)
    html = browser.page_source
    doc = pq(html)
    a = doc('.schedule-info')
    urls = []
    for i in range(len(a)):
        link = a.eq(i).attr('href')
        if not link.startswith('https://'):
            link = 'https://mdianying.baidu.com' + link
        urls.append(link)

        for url in urls:
            get_details(url, browser, movie_id, timestamp)
            time.sleep(1)


def get_details(url, browser, movie_id, timestamp):
    browser.get(url)
    html = browser.page_source
    doc = pq(html)
    print(url)
    cinema_name = doc('.cinema-name').text()
    print(cinema_name)
    changci = doc('.schedule.date-{}000.movie-{}'.format(timestamp, movie_id)).find('.daily-schedule')
    print(len(changci))
    for i in range(len(changci)):
        time = changci.eq(i).find('.time').text()
        print(time)
        price = changci.eq(i).find('.price').text().split(' ')
        print('价格：', price[1])


if __name__ == "__main__":
    get_index()
