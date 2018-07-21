#!flask/bin/python
# -*- coding: utf-8 -*-
__author__ = 'kbson'
__blog__ = 'https://www.along.party'
__email__ = 'kbsonlong@gmail.com'

from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request


###使用ImagesPipeline下载图片
class MyImagesPipeline(ImagesPipeline):
    default_headers = {
        'accept': 'image/webp,image/*,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, sdch, br',
        'accept-language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'cookie': 'bid=yQdC/AzTaCw',
        'referer': 'https://92zfl.com/luyilu/2015/0218/1.html',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    }

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            self.default_headers['referer'] = image_url
            yield Request(image_url, headers=self.default_headers,meta={'item': item, 'index': item['image_urls'].index(image_url)})

    ##自定义存储路径和原图片名称
    def file_path(self, request, response=None, info=None):
        item = request.meta['item']  # 通过上面的meta传递过来item
        index = request.meta['index']
        image_guid = request.url.split('/')[-1]
        down_file_name = u'{0}/{1}'.format(item['images'][index], image_guid)
        # down_file_name = u'full/{0}/{1}'.format(index, image_guid)
        return down_file_name

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item