#!flask/bin/python
# -*- coding: utf-8 -*-
__author__ = 'kbson'
__blog__ = 'https://www.along.party'
__email__ = 'kbsonlong@gmail.com'
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from ImageSpider.spiders.tencent import TencentSpider
from ImageSpider.models import db_connect,ArticleRule
from sqlalchemy.orm import sessionmaker

if __name__ == '__main__':
    settings = get_project_settings()
    ##连接数据库获取爬虫规则
    db = db_connect()
    Session = sessionmaker(bind=db)
    session = Session()
    rules = session.query(ArticleRule).filter(ArticleRule.enable == 1).all()
    session.close()

    configure_logging()
    runner = CrawlerRunner(settings)

    # runner.crawl(MfwSpider)
    # runner.crawl(LpSpider)

    for rule in rules:
        runner.crawl(TencentSpider,rule=rule)
        print(rule.name)

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    reactor.run()