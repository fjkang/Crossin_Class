# coding=utf-8

import requests
import bs4
import threading

header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) \
                        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}


def get_pic_urls(url):
    req = requests.get(url, headers=header)
    page = req.text

    soup = bs4.BeautifulSoup(page, 'lxml')
    soup_img = soup.find_all('img', attrs={'srcset':True})
    pics = []
    for img in soup_img:
        pic_url = img['src']
        pics.append(pic_url)

    return pics

def download_pic(url):

    req = requests.get(url)
    content = req.content
    name = url.split('/')[-1]
    with open(name, 'wb')as f:
        f.write(content)

def main():

    url = 'https://pixabay.com/'
    pic_urls = get_pic_urls(url)

    # 多线程

    threads = []
    for i in pic_urls:
        t = threading.Thread(target=download_pic,args=(i,))
        threads.append(t)

    for i in threads:
        i.start()

if __name__ == '__main__':
    main()