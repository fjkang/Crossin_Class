from bs4 import BeautifulSoup
import requests
from threading import Thread



def down_pic(link):
    pic = requests.get(link)
    filename = link.split('/')[-1]
    print('download:'+filename)
    with open('pixabay_pic/' + filename, 'wb') as f:
        f.write(pic.content)
        print(filename + '  saved')


def pic_url(soup):
    pics = []
    for img in soup.find_all('img',attrs={'srcset':True}):
        pic = img['src']
        pics.append(pic)
    return pics



def main():
    url = "https://pixabay.com/"
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'lxml')
    pics = pic_url(soup)

    threads = []
    for link in pics:
        t = Thread(target=down_pic, args=(link,))
        threads.append(t)

    for down in threads:
        down.start()

if __name__ == '__main__':
    main()