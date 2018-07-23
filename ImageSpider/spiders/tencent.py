# -*- coding: utf-8 -*-
import scrapy

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule
from ImageSpider.items import Article



class TencentSpider(CrawlSpider):
    name = 'tencent'

    def __init__(self, rule):
        self.rule = rule
        self.name = rule.name
        self.allowed_domains = rule.allow_domains.split(",")
        self.start_urls = rule.start_urls.split(",")
        rule_list = []

        # 添加`下一页`的规则
        if rule.next_page:
            rule_list.append(Rule(LinkExtractor(restrict_xpaths=rule.next_page)))
        # 添加抽取文章链接的规则
        rule_list.append(Rule(LinkExtractor(
            allow=[rule.allow_url],
            restrict_xpaths=[rule.extract_from]),
            callback='parse_item'))
        self.rules = tuple(rule_list)

        super(TencentSpider, self).__init__()


    # 使用CrawlSpider时，不能写parse方法，因为CrawlSpider源码中已经有了parse方法，会覆盖导致程序不能跑
    def parse_item(self, response):
        article = Article()
        article["url"] = response.url

        article["title"] = response.xpath(self.rule.title_xpath).extract()

        article["body"] = response.xpath(self.rule.body_xpath).extract()

        # author = response.xpath('//span[@class="muted"][2]/a/text()').extract()
        article["author"] = response.xpath(self.rule.author_xpath).extract()

        article["publish_time"] = response.xpath(self.rule.publish_time_xpath).extract()

        article["source_site"] = self.rule.source_site

        return article

