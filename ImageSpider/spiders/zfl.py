# -*- coding: utf-8 -*-
import scrapy
#from urllib import request
from ImageSpider.items import DuplicatesItem,ZflImgsItem


class ZflSpider(scrapy.Spider):
    name = 'zfl'
    allowed_domains = ['92zfl.com','sozfl.com']
    start_urls = ['https://92zfl.com/luyilu/']
    # start_urls = ['https://sozfl.com/serch.php?keyword=%CB%BD%C8%CB%CD%E6%CE%EF&page=1']

    def parse(self, response):
        item = DuplicatesItem()

        ##获取到下一页地
        next_page_url = response.xpath('//li[@class="next-page"]/a/@href').extract_first()
        # page_num=int(next_page_url.split('.')[0].split('_')[-1])
        # if next_page_url and page_num < 3:
        if next_page_url :
            next_page_url = response.urljoin(next_page_url)
            #将url传递给自己self.parse进行解析
            yield scrapy.Request( next_page_url,callback=self.parse)
        else:
            print(response.url)

        ###对本页面进行解析获取相关内容
        pagelist = response.xpath('/html/body/section/div/div/article/header/h2/a')
        for page in pagelist:
            url = page.xpath('./@href').extract_first()
            title = page.xpath('./@title').extract_first()
            item['url'] = url
            item['title'] = title
            yield scrapy.Request(response.urljoin(url),callback=self.Second_pages)

    def Second_pages(self,response):

        next_page_url = response.xpath('//li[@class="next-page"]/a/@href').extract_first()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(next_page_url, callback=self.Second_pages)
        else:
            print(response.url)

        imageslist = response.xpath('/html/body/section/div/div/article/p/img')

        for image in imageslist:
            list_imgs = image.xpath('./@src').extract()
            image_alt = image.xpath('./@alt').extract()
            item = ZflImgsItem()
            item['image_urls'] = list_imgs
            item['images'] = image_alt
            yield item
