import time
import os
import threading

from selenium import webdriver
from bs4 import BeautifulSoup
import urllib

url = 'https://mm.taobao.com/search_tstar_model.htm'
path = 'C:\phantomjs\\bin\phantomjs.exe'

driver = webdriver.PhantomJS(path, service_args=['--load-images=no'])
driver.set_window_size(1920, 2000)

all_models = []
for i in range(1):
    driver.get(url)
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'lxml')

    items = soup.find_all(class_='item')
    all_models.extend(items)
    driver.find_element_by_link_text('下一页 >').click()
    time.sleep(1)

for item in all_models[:2]:
    link = item.find('a').get('href')
    item_img = item.find('img')
    img = item_img.get('data-ks-lazyload') or item_img.get('src')
    name = item.find(class_='name').get_text()
    city = item.find(class_='city').get_text()

    dir_city = 'photos/{}'.format(city)
    if not os.path.exists(dir_city):
        os.mkdir(dir_city)
    dir_name = '{}/{}'.format(dir_city, name)
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    if img.startswith('//'):
        img = 'http:' + img
    filename = '{}/{}'.format(dir_name, img.split('/')[-1])

    print('get', img)
    if not os.path.exists(filename):
        urllib.request.urlretrieve(img, filename)

    if link.startswith('//'):
        link = 'http:' + link
    print('get', link)
    driver.get(link)
    time.sleep(1)
    soup_detail = BeautifulSoup(driver.page_source, 'lxml')
    all_img = soup_detail.find(class_='mm-aixiu-content').find_all('img')
    for pic in all_img:
        print(pic.get('src'))
        pic_url = pic.get('src')
        if pic_url.startswith('//'):
            pic_url = 'http:' + pic_url
        filename = '{}/{}'.format(dir_name, pic_url.split('/')[-1])
        if not os.path.exists(filename):
            threading.Thread(target=urllib.request.urlretrieve, args=(pic_url, filename)).start()
            # urllib.request.urlretrieve(pic_url, filename)
            print(threading.active_count())
            while threading.active_count() > 3:
                time.sleep(3)