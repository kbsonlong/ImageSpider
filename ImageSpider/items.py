# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DuplicatesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = "insert into zfl (title, url) VALUES (%s, %s);"
        params = (self["title"], self["url"])
        return insert_sql, params


class ZflImgsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_paths = scrapy.Field()

class TencentItem(scrapy.Item):
    # 职位
    name = scrapy.Field()
    # 详情链接
    positionlink = scrapy.Field()
    #职位类别
    positiontype = scrapy.Field()
    # 人数
    peoplenum = scrapy.Field()
    # 工作地点
    worklocation = scrapy.Field()
    # 发布时间
    publish = scrapy.Field()

