# -*- coding: utf-8 -*-

# Scrapy settings for ImageSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'ImageSpider'

SPIDER_MODULES = ['ImageSpider.spiders']
NEWSPIDER_MODULE = 'ImageSpider.spiders'


# LOG_FILE = 'imagespider.log'
# LOG_LEVEL = 'INFO'
# LOG_ENCODING = 'utf-8'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'ImageSpider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32   #并发请求数，默认32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3          #等待3s访问网站
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16    # 单domain的线程数，默认为16
#CONCURRENT_REQUESTS_PER_IP = 16        #单IP的线程数，默认为16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False                 #禁止cookies能减少CPU使用率及Scrapy爬虫在内存中记录的踪迹，提高性能。

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-ENCODING': 'gzip, deflate, sdch, br',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'COOKIE': 'bid=yQdC/AzTaCw',
    'USER-AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',

}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   'ImageSpider.RotateUserAgentMiddleware.RotateUserAgentMiddleware': 543,
}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'ImageSpider.middlewares.ImagespiderDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 'ImageSpider.pipelines.ImagespiderPipeline': 300,
   # 'ImageSpider.pipelines.XwnspiderPipeline': 300,
   # 'ImageSpider.pipelines.TencentPipeline': 300,
   #  'ImageSpider.Imagepipelines.DuplicatesPipeline': 100,
    'ImageSpider.Imagepipelines.MyImagesPipeline': 301,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


IMAGES_STORE = 'img'                                    # 图片存储路径
IMAGES_EXPIRES = 90                                     # 过期天数
# IMAGES_MIN_HEIGHT = 100                               # 图片的最小高度
# IMAGES_MIN_WIDTH = 100                                # 图片的最小宽度
# 图片的尺寸小于IMAGES_MIN_WIDTH*IMAGES_MIN_HEIGHT的图片都会被过滤

RETRY_ENABLED = False                                    #禁止重试
DOWNLOAD_TIMEOUT = 15                                    #下载超时时间
# JOBDIR = 'job_process/001'