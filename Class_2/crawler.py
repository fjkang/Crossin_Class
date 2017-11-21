from bs4 import BeautifulSoup
import requests
import urllib.request
from threading import Thread

url = "http://jandan.net/pic"

def down_pic(link):
    print("downloading:" + link)
    filename = link.split('/')[-1]
    retries = 0
    while retries < 3:
        try:
            pic = requests.get('http:' + link, timeout=30)
            with open('pics/' + filename, 'wb') as f:
                f.write(pic.content)
            urllib.request.urlretrieve('http:' + link, 'pics/' + filename)
        except requests.exceptions.RequestException as e:
            retries += 1
            print(e)
            print(filename, "failed")
        else:
            print(filename, "saved")
            break

for i in range(3):
    print(url)
    req = requests.get(url)
    html = req.text

    soup = BeautifulSoup(html, "lxml")
    result = soup.find_all('a', class_='view_img_link')

    for link in result:
        link = link.get('href')
        t = Thread(target=down_pic, args=(link,))
        t.start()
        current_page = soup.find_all('span', class_='current-comment-page')
        current_page = current_page[0].text
        next_page = int(current_page.strip('[]')) -1

        url = "http://jandan.net/pic/page-%d" % next_page


