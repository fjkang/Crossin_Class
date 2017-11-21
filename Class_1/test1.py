from lxml import etree

with open('test1.txt' ,'r' ,encoding='utf-8') as f:
    html = f.read()

xp = etree.HTML(html)

article = xp.xpath('//p')[1]
# article = xp.xpath('/section/article/p')[1]
# article = xp.xpath('body/section/article/p')[1]
# article = xp.xpath('//p[@class="Chinese"]')
# a = article.xpath('text()')
a = article.text
print(a)