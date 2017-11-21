from lxml import etree
import requests
import time

url = 'https://www.qiushibaike.com/'
page = 1
data_all = ""

for i in range(10):

    req = requests.get(url)
    html = req.text
    # print(html)

    tree = etree.HTML(html)

    div_xpath = tree.xpath('//div[@class="article block untagged mb15"]')

    for div in div_xpath:
        author_name = div.xpath('.//div[@class="author clearfix"]//h2/text()')[0]
        if author_name != "匿名用户":
            author_age = div.xpath('.//div[@class="author clearfix"]/div/text()')[0]
            author_sex = div.xpath('.//div[@class="author clearfix"]/div/@class')[0]
            if author_sex == 'articleGender manIcon':
                sex = "男"
            else:
                sex = "女"
        else:
            author_age = "无"
            sex = "无"
        data_all += ("用户名：" + author_name + '\n')
        data_all += ("年龄：" + author_age + '\n')
        data_all += ("性别：" + sex + '\n')
        # print(data_all)

        content = div.xpath('.//div[@class="content"]/span/text()')[0]
        data_all += (content + '\n')
        # print(data_all)

        stats = div.xpath('.//div[@class="stats"]/span[@class="stats-vote"]/i/text()')
        if stats:
            data_all += ("好笑：" +stats[0] +'\n')
        # print(data_all)

        coment = div.xpath('.//div[@class="stats"]/span[@class="stats-comments"]/a/i/text()')
        if coment:
            data_all += ("评论：" + coment[0] +'\n')
        # print(data_all)

    data_all += ('======================' +'\n')
    data_all += ("-PAGE"+str(page)+"-"+'\n')

    page += 1
    url = 'https://www.qiushibaike.com/8hr/page/%d' % page
    time.sleep(1)

with open('qiushibaike.txt' ,'w' ,encoding='utf-8') as f:
    f.write(data_all)