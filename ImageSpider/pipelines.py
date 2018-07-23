# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import requests

class TencentPipeline(object):
    def __init__(self):
        self.filename = open("tencent.json", "w")

    def process_item(self, item, spider):
        text = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        try:
            self.filename.write(text.encode('utf-8'))
        except:
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
    def __init__(self):
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
        # print(insert_sql,params)
        cursor.execute(insert_sql, params)


    def handle_error(self, failure, item, spider):
        #处理异步插入的异常
        print (failure)


from ImageSpider.models import Proxy_pool,db_connect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from scrapy.exceptions import DropItem


class XiciPipline(object):
    def __init__( self ):  # 执行爬虫时
        self.engine = db_connect()
        self.session = sessionmaker(bind=self.engine)
        self.sess = self.session()
        Base = declarative_base()
        # 动态创建orm类,必须继承Base, 这个表名是固定的,如果需要为每个爬虫创建一个表,请使用process_item中的
        self.Proxy = type('proxypools', (Base, Proxy_pool),
                            {'__tablename__': 'proxypools'})


    def process_item( self, item, spider ):  # 爬取过程中执行的函数
        http_url = "http://www.baidu.com"
        proxy_url = "{2}://{0}:{1}".format(item["ip"], item["port"], item["proxy_type"])
        try:
            proxy_dict = {
                "http": proxy_url,
            }
            response = requests.get(http_url, proxies=proxy_dict,timeout=3)
        except Exception as e:
            print ("invalid ip and port")
            raise DropItem("Duplicate book found:%s".format(item))
        else:
            code = response.status_code
            if code >= 200 and code < 300:
                print ("effective ip")
                self.sess.add(self.Proxy(**item))
                self.sess.commit()
            else:
                print  ("invalid ip and port")
                raise DropItem("Duplicate book found:%s".format(item))

