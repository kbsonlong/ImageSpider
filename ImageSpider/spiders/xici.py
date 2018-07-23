# -*- coding: utf-8 -*-
import scrapy
import requests
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ImageSpider.items import Xici


class XiciSpider(scrapy.Spider):
    name = "xici"
    allowed_domains = ["xicidaili.com"]
    start_urls = (
        'http://www.xicidaili.com/',
    )

    def start_requests(self):
        res = []
        for i in range(1, 2):
            url = 'http://www.xicidaili.com/nn/%d'%i
            req = scrapy.Request(url)
            # 存储所有对应地址的请求
            res.append(req)
        return res



    def parse(self, response):
        table = response.xpath('//*[@id="ip_list"]')[0]
        trs = table.xpath('//tr')[1:]
        items = []
        for tr in trs:
            pre_item = Xici()
            pre_item['ip'] = tr.xpath('./td[2]/text()').extract_first()
            pre_item['port'] = int(tr.xpath('td[3]/text()').extract_first())
            pre_item['proxy_type'] = tr.xpath('td[6]/text()').extract_first()
            pre_item['speed'] = tr.xpath('td[7]/div/@title').re('\d+\.\d*')[0]
            items.append(pre_item)
        return items

