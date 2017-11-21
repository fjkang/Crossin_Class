import time
import os

from selenium import webdriver
import urllib
from pyquery import PyQuery as pq

path = r'C:\phantomjs\bin\phantomjs.exe'
url = 'http://zu.sh.fang.com/'

browser = webdriver.PhantomJS(path, service_args=['--load-images=no'])
browser.set_window_size(1920, 2000)
browser.get(url)
time.sleep(1)
browser.find_element_by_link_text('闵行').click()
time.sleep(1)

for i in range(5):
    html = browser.page_source
    doc = pq(html)
    houselist = doc('.houseList').find('.list.hiddenMap.rel').items()
    for house in houselist:
        img = house.find('.b-lazy').attr('data-src')
        address = house.find('.gray6.mt20').text().replace(' ', '')
        price = house.find('.price').text()
        filename = 'fangtianxia/{}{}元-月.jpg'.format(address, price)
        if not os.path.exists(filename):
            try:
                print('get:', filename)
                urllib.request.urlretrieve(img, filename)
            except Exception as e:
                print(e)
                continue
    print('第{}页'.format(i+1))
    browser.find_element_by_link_text('下一页').click()
    time.sleep(1)
