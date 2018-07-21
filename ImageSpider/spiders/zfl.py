# -*- coding: utf-8 -*-
import scrapy
#from urllib import request
from ImageSpider.items import ImagespiderItem,DoubanImgsItem


class ZflSpider(scrapy.Spider):
    name = 'zfl'
    allowed_domains = ['92zfl.com','sozfl.com']
    start_urls = ['https://92zfl.com/luyilu/']
    #start_urls = ['https://sozfl.com/serch.php?keyword=%BC%AB%C6%B7%B4%F3%D0%D8']

    def parse(self, response):
        item = ImagespiderItem()

        ##获取到下一页地
        next_page_url = response.xpath('//li[@class="next-page"]/a/@href').extract_first()
        page_num=int(next_page_url.split('.')[0].split('_')[-1])
        if next_page_url and page_num < 3:
        #if next_page_url :
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
            yield scrapy.Request(response.urljoin(url),callback=self.Second_pages)

    def Second_pages(self,response):

        next_page_url = response.xpath('//li[@class="next-page"]/a/@href').extract_first()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(next_page_url, callback=self.Second_pages)
        else:
            print(response.url)

        imageslist = response.xpath('/html/body/section/div/div/article/p')

        for image in imageslist:
            list_imgs = image.select('./img/@src').extract()
            image_alt = image.select('./img/@alt').extract()
            item = DoubanImgsItem()
            item['image_urls'] = list_imgs
            item['images'] = image_alt
            yield item
