import time

import requests
from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def get_index(cityname, moviename, timestamp):
    url = 'https://h5.m.taopiaopiao.com/app/moviemain/pages/index/index.html'

    path = r"C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chrome.exe"
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    # mobileEmulation = {'deviceName': 'iPad'}
    # chrome_options.add_experimental_option('mobileEmulation', mobileEmulation)
    browser = webdriver.Chrome(chrome_options=chrome_options)

    # path = r"C:\phantomjs\bin\phantomjs.exe"
    # service_args = []
    # service_args.append('--load-images=no')  ##关闭图片加载
    # browser = webdriver.PhantomJS(path, service_args=service_args)
    browser.set_window_size(1600, 1000)
    wait = WebDriverWait(browser, 10)
    browser.get(url)
    wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, 'movielist-wrapper'))
    )
    time.sleep(2)
    html = browser.page_source
    doc = pq(html)
    movies = doc('.movielist-wrapper .movie-info')
    for i in range(len(movies)):
        showname = movies.eq(i).find('.show-name').text()
        link = movies.eq(i).find('.button').attr('href')
        if showname == moviename:
            cinema_links = get_cinema(browser, link, wait)
            break
    print('共{}间影院有上映{}'.format(len(cinema_links), moviename))
    for link in cinema_links:
        try:
            get_details(browser, link, timestamp, wait)
        except Exception as e:
            print(e)
            continue
        time.sleep(1)


def get_cinema(browser, link, wait):
    browser.get(link)
    time.sleep(2)
    citylist = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, 'selector-i-arrow'))
    )
    citylist.click()
    location = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//li[@data-cityname="{}"]'.format(cityname)))
    )
    location.click()
    time.sleep(5)
    wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, 'cinema-list-ul'))
    )
    html = browser.page_source
    doc = pq(html)
    cinema_list = doc('.list-normal')
    print(len(cinema_list))
    links = []
    for i in range(len(cinema_list)):
        # cinma_name = cinema_list.eq(i).find('.list-title ').text()
        cinema_link = cinema_list.eq(i).find('.list-item-in').attr('data-href')
        links.append(cinema_link)
    return links


def get_details(browser, link, timestamp, wait):
    browser.get(link)
    wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, 'schedules-list'))
    )
    html = browser.page_source
    doc = pq(html)
    print(link)
    cinema_name = doc('.cinema-name').text()
    print(cinema_name)
    showname = doc('.showname').text()
    print(showname)
    ul = doc('.schedules-item-wrap').filter(lambda i: pq(this).attr('data-schedule') == '{}000'.format(timestamp))
    # print(len(ul))
    changci = ul.find('.item-wrap')
    for i in range(len(changci)):
        start = changci.eq(i).find('.item-clock').text()
        end = changci.eq(i).find('.item-end').text()
        price = changci.eq(i).find('.price').text()
        print('{}-{}'.format(start, end))
        print('价格:', price)


if __name__ == "__main__":
    cityname = '广州'
    moviename = '正义联盟'
    date = '2017-11-24'
    timeArray = time.strptime(date, "%Y-%m-%d")
    timestamp = int(time.mktime(timeArray))
    get_index(cityname, moviename, timestamp)
