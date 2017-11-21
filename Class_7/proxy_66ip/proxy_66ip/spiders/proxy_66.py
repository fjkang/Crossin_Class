# -*- coding: utf-8 -*-
import scrapy
import pymongo
from scrapy.http import Request, TextResponse
from pyquery import PyQuery as pq
from proxy_66ip.items import Proxy66IpItem

class Proxy66Spider(scrapy.Spider):
    name = 'proxy_66'
    allowed_domains = ['http://www.66ip.cn']
    start_urls = ['http://www.66ip.cn/']

    def parse(self, response):
        ul = response.xpath('//ul[@class="textlarge22"]')[0]
        urls = ul.xpath('./li[not(@class)]/a/@href')
        for url in urls:
            url = url.extract()
            yield Request('http://www.66ip.cn' + url, callback=self.getDetail, dont_filter=True)

    def getDetail(self, response):
        print(response.url)
        doc = pq(response.text)
        trs = doc('div.footer tr')
        item = Proxy66IpItem()
        for i in range(1, len(trs)):
            tds = trs.eq(i).find('td')
            item['ip'] = tds.eq(0).text()
            item['port'] = tds.eq(1).text()
            item['location'] = tds.eq(2).text()
            item['port_type'] = tds.eq(3).text()
            yield item


