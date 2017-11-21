import requests
from lxml import etree

url = 'http://jandan.net/duan'

for i in range(3):
    data_all = ''

    req = requests.get(url)
    html = req.text

    tree = etree.HTML(html)
    result = tree.xpath('//li//div[@class="text"]')

    for div in result:
        author = div.xpath('../div[@class="author"]/strong/text()')
        data_all += (author[0] +':\n')
        content = div.xpath('p/text()')
        for p in content:
            data_all += p
        data_all += '\n\n'


    current_page = tree.xpath('//span[@class="current-comment-page"]/text()')
    next_page = int(current_page[0].strip('[]')) - 1
    url = 'http://jandan.net/duan/page-%d' % next_page

# print(data_all)
with open('jokes.txt' ,'w',encoding='utf-8') as f:
    f.write(data_all)