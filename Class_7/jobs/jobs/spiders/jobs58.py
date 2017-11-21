# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from jobs.items import JobsItem


class Jobs58Spider(scrapy.Spider):
    name = 'jobs58'
    allowed_domains = ['58.com']
    start_urls = ['http://sh.58.com/job']

    for i in range(2, 71):
        start_urls.append('http://sh.58.com/job/pn{}'.format(i))

    def parse(self, response):
        links = response.xpath('//div[@class="job_name clearfix"]/a/@href').extract()
        for link in links:
            yield Request(link, callback=self.get_Detail)

    def get_Detail(self, response):
        print('got', response.url, response)
        title = response.xpath('//span[@class="pos_title"]/text()')[0].extract()
        try:
            salary = response.xpath('//span[@class="pos_salary"]/text()')[0].extract()
        except:
            salary = '0'
        num = response.xpath('//span[@class="item_condition pad_left_none"]/text()')[0].extract()
        edu = response.xpath('//span[@class="item_condition"]/text()')[0].extract()
        exp = response.xpath('//span[@class="item_condition border_right_None"]/text()')[0].extract()
        area = response.xpath('//span[@class="pos_area_item"]/text()').extract()
        # print(title, salary, num, edu, exp, area)
        item = JobsItem()
        item['title'] = title.strip()
        item['salary'] = salary.strip()
        item['num'] = num.strip('招人 ')
        item['edu'] = edu.strip()
        item['exp'] = exp.strip()
        item['area'] = area
        yield item