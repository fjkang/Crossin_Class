import requests
import threading

url_1 = 'https://www.zhihu.com/api/v4/members/'
url_2 = '/followers?include=data%5B%2A%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit=20&offset='

headers = {
    'Cookie':'aliyungf_tc=AQAAAKn7eTlVywYAcsJJ3/Ei2MSX/+Gq; q_c1=da6daac315b34dcf9d3769ffe3bb6dc6|1500614704000|1500614704000; _xsrf=253d8ff3d4c7ca08209af8019d1ba0ae; r_cap_id="ZDhlYmRmNTJlNDkyNDU4NzhjYjljYmRmNTZmYWY5YTY=|1500614704|46533c2784f710ca163d4ef5052ce0516d88379f"; cap_id="ZDM0YzA5Y2EzOTdlNGYzMThjOWM3MGNhNzE0MmQzMzk=|1500614704|17dd146151dc8e5cd3fae2ee736f346eb17647dd"; d_c0="ADCCKHv6GAyPTk1GxLpQ6ZS5szArjc7YkRQ=|1500614705"; _zap=718570b4-fce4-4162-a564-8e003b14053a; __utma=51854390.953576744.1500614706.1500614706.1500614706.1; __utmb=51854390.0.10.1500614706; __utmc=51854390; __utmz=51854390.1500614706.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=51854390.000--|3=entry_date=20170721=1; z_c0=Mi4wQURDQktVaUVvQWNBTUlJb2Vfb1lEQmNBQUFCaEFsVk5VeDJaV1FCTFp2cC04WGNOWUtRMVZ4VEZUQnkzVUZoMWhB|1500614739|8ccf624c676de2334212550b10a2632bc41a2258; n_c=1; _xsrf=253d8ff3d4c7ca08209af8019d1ba0ae',
    'Host':'www.zhihu.com',
    'Referer':'https://www.zhihu.com/people/crossin/followers',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36'
}

def crawl(url):
    global to_crawl, crawled, finished
    req = requests.get(url, headers=headers)
    data = req.json()

    for user in data['data']:
        if user['follower_count'] > 600000:
            token = user['url_token']
            if token not in to_crawl and token not in crawled:
                print(user['name'])
                to_crawl.append(token)
                finished.set()
                print("add token", token)

    return data['paging']


def get_following(user):
    global to_crawl, crawled
    print('crawling:', user)

    url = url_1 + user + url_2 + '0'
    paging = crawl(url)
    totals = paging['totals']
    count = 20

    while count < totals and count <200:
        url = url_1 + user + url_2 + str(count)
        t = threading.Thread(target=crawl, args=(url,))
        t.start()
        count += 20

    print('to crawl:', to_crawl)
    print('crawled:', crawled)

to_crawl = ['crossin']
crawled = []
finished = threading.Event()

while len(to_crawl) > 0:
    user = to_crawl.pop()
    crawled.append(user)
    get_following(user)

    while len(to_crawl) == 0 and threading.active_count() > 1:
        print(to_crawl)
        print("wait:", threading.active_count())
        finished.clear()
        finished.wait(3)

