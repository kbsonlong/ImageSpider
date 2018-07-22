# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class TencentPipeline(object):
    def __init__(self):
        self.filename = open("tencent.json", "w")

    def process_item(self, item, spider):
        text = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        self.filename.write(text)
        return item

    def close_spider(self, spider):
        self.filename.close()


class ImagespiderPipeline(object):
    def __init__(self):
        self.file = open('zfl.json', 'w+')

    def process_item(self, item, spider):
        if spider.name == 'zfl':
            content = json.dumps(dict(item), ensure_ascii=False) + "\n"
            self.file.write(content)
        return item

    def close_spider(self, spider):
        self.file.close()

class XwnspiderPipeline(object):
    def __init__(self):
        self.file = open('xwn.json', 'w+')

    def process_item(self, item, spider):
        if spider.name == 'xwn':
            content = json.dumps(dict(item), ensure_ascii=False) + "\n"
            self.file.write(content)
        return item

    def close_spider(self, spider):
        self.file.close()


##实现 MySQL 存储的异步操作

import pymysql
from twisted.enterprise import adbapi

class MysqlTwistedPipline(object):
    def __init__(self, ):
        dbparms = dict(
            host='www.along.party',
            db='demo',
            user='root',
            passwd='kbsonlong',
            port = 8080,
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor, # 指定 curosr 类型
            use_unicode=True,
        )
        # 指定擦做数据库的模块名和数据库参数参数
        self.dbpool = adbapi.ConnectionPool("pymysql", **dbparms)

    # 使用twisted将mysql插入变成异步执行
    def process_item(self, item, spider):
        # 指定操作方法和操作的数据
        query = self.dbpool.runInteraction(self.do_insert, item)
        # print(query)
        # 指定异常处理方法
        query.addErrback(self.handle_error, item, spider) #处理异常


    def do_insert(self, cursor, item):
        #执行具体的插入
        #根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql, params = item.get_insert_sql()
        print(insert_sql,params)
        cursor.execute(insert_sql, params)


    def handle_error(self, failure, item, spider):
        #处理异步插入的异常
        print (failure)