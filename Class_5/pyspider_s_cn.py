#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-11-02 16:16:48
# Project: s_cn_test

from pyspider.libs.base_handler import *
import re


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('s.cn', callback=self.index_page, validate_cert=False)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        pat1 = "https://www.s.cn/(\w+)-brand.html"
        brand = re.match(pat1, response.url)
        if brand:
            brand = brand.group(1)
        for each in response.doc('a[href^="http"]').items():
            link = each.attr.href
            pat2 = 'https://www.s.cn/{}-\w+-*\w+.html$'.format(brand)
            if '-brand.html' in link:
                self.crawl(each.attr.href, callback=self.index_page, validate_cert=False)
            elif re.match(pat2, link):
                self.crawl(each.attr.href, callback=self.detail_page, validate_cert=False)

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
            "price":  response.doc('span.price1').text(),
            "canshu": response.doc('div.proshow-canshu > ul').text(),
        }
