import time

from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def get_index(cityname, moviename, timestamp):
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.set_window_size(1600, 1000)
    wait = WebDriverWait(browser, 10)

    citycode = get_citycode(browser, cityname)
    city_url = '&c={}&cc={}'.format(citycode, citycode)

    url = 'https://mdianying.baidu.com/?page=movie' + city_url
    browser.get(url)

    movies_ul = wait.until(
        EC.presence_of_element_located((By.XPATH, '//ul[@class="movie-list"]'))
    )
    html = browser.page_source
    doc = pq(html)
    movies = doc('.movie-info-wrapper')
    movie_id = ''
    for i in range(len(movies)):
        moive = movies.eq(i).find('.movie-name-text').text()
        movie_link = movies.eq(i).find('.movie-buy-btn').attr('data-href')

        if moive == moviename:
            movie_id = movie_link.strip('/movie/schedule?movieId=')
            url = 'https://mdianying.baidu.com' + movie_link \
                  + '&kehuduan=&sfrom=wise_shoubai&sub_channel=&from=webapp&source=' \
                  + city_url
            urls = get_cinema(browser, url, wait)
            break
    print('共{}间影院有上映{}'.format(len(urls), moviename))
    for url in urls:
        get_details(url, browser, movie_id, timestamp)
        time.sleep(1)


def get_citycode(browser, cityname):
    browser.get('https://mdianying.baidu.com/city/choose')
    html = browser.page_source
    doc = pq(html)
    city_list = doc('.city-item')
    for i in range(len(city_list)):
        city = city_list.eq(i).text()
        citycode = city_list.eq(i).attr('data-citycode')
        if city == cityname:
            return citycode


def get_cinema(browser, url, wait):
    browser.get(url)
    js = "var q=document.documentElement.scrollTop=100000"
    for i in range(5):
        browser.execute_script(js)
        time.sleep(1)
    cinema_list = wait.until(
        EC.presence_of_all_elements_located((By.XPATH, '//section[@id="schedule"]'))
    )
    html = browser.page_source
    doc = pq(html)
    a = doc('.schedule-info')
    urls = []
    for i in range(len(a)):
        link = a.eq(i).attr('href')
        if not link.startswith('https://'):
            link = 'https://mdianying.baidu.com' + link
        urls.append(link)
    return urls


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
        print('价格:', price[1])


if __name__ == "__main__":
    cityname = '广州'
    moviename = '正义联盟'
    date = '2017-11-24'
    timeArray = time.strptime(date, "%Y-%m-%d")
    timestamp = int(time.mktime(timeArray))
    get_index(cityname, moviename, timestamp)
