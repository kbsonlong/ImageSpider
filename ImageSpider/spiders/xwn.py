# -*- coding: utf-8 -*-
import scrapy
from ImageSpider.items import DuplicatesItem

class XwnSpider(scrapy.Spider):
    name = 'xwn'
    allowed_domains = ['www.along.party']
    start_urls = ['https://www.along.party/?cat=2']

    def parse(self, response):
        item = DuplicatesItem()
        pagelist = response.xpath('//article[@class="excerpt"]')
        for page in pagelist:
            item['url'] = page.xpath('./header/h2/a/@href').extract_first()
            item['title'] = page.xpath('./header/h2/a/@title').extract_first()
            yield item
        next_page_url = response.xpath('//li[@class="next-page"]/a/@href').extract_first()

        if next_page_url:
            yield scrapy.Request(next_page_url,callback=self.next_page)
        else:
            print(response.url)

    def next_page(self,response):
        item = DuplicatesItem()
        pagelist = response.xpath('//article[@class="excerpt"]')
        for page in pagelist:
            item['url'] = page.xpath('./header/h2/a/@href').extract_first()
            item['title'] = page.xpath('./header/h2/a/@title').extract_first()
            yield item
        next_page_url = response.xpath('//li[@class="next-page"]/a/@href').extract_first()

        if next_page_url:
            yield scrapy.Request( next_page_url, callback=self.parse)
        else:
            print(response.url)
