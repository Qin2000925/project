# -*- coding: utf-8 -*-

# Scrapy settings for project project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'project'

SPIDER_MODULES = ['project.spiders']
NEWSPIDER_MODULE = 'project.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'project (+http://www.yourdomain.com)'

# Obey robots.txt rules
# ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Host': 'www.zhihu.com',
    # 'Referer': 'https://www.zhihu.com/api/v4/members/chi-wan-fan-la/followers?',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
}

MYSQL_USER = 'root'
MYSQL_PASSWORD = 'qinjiahu521'
MYSQL_DB = 'python'
MYSQL_HOST = '127.0.0.1'


COOKIES = {
    't': '3fc63797b2e5c67411548f4b4275d7d5; ',
    'cna': 'Xt+qEvL2blkCAW8AXbZBMPF6; ',
    'hng': 'CN%7Czh-CN%7CCNY%7C156; ',
    'thw': 'cn; ',
    'lgc': '%5Cu65E7%5Cu65F6%5Cu5149%5Cu7684%5Cu5E05%5Cu6C14%5Cu5C11%5Cu5E7420277; ',
    'tracknick': '%5Cu65E7%5Cu65F6%5Cu5149%5Cu7684%5Cu5E05%5Cu6C14%5Cu5C11%5Cu5E7420277; ',
    'tg': '0; ',
    'x': 'e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; ',
    'UM_distinctid': '160c5669cb1bf-0e3f84ae42ef72-1e291c08-100200-160c5669cb2609; ',
    'enc': 'fXJnYb93799Yng8V5yymcGmDo6Vy90QRZIKb04bnUriwIFz%2BuXrBfjXVoxVlhu%2BCZ%2F8wkSpjYDanfY7w26zgyg%3D%3D; ',
    'miid': '629898394606107612; ',
    'v': '0; ',
    'cookie2': '1f85d3dbdbbcf6042e0af09368e41d82; ',
    '_tb_token_': 'b953d03ee1fe; ',
    'uc3': 'sg2=UtQFQ01BAoVPBSEh7j07tB8X0%2BPR46cRBlVkGWhAvdQ%3D&nk2=3Rc9HSQUdmIr0LWwXMkdZ5VYdykD&id2=UU8NYS8hCF5h6g%3D%3D&vt3=F8dBzLllYz4KSVud7Bw%3D&lg2=VT5L2FSpMGV7TQ%3D%3D; ',
    'existShop': 'MTUxNjU0ODQxMw%3D%3D; ',
    'uss': 'W878X7vNMCcG1R%2F4IdtCYqhqZqyiTXWQUI%2FlNBt5RSd0jmxhzpzrG%2FYYaQ%3D%3D; ',
    'sg': '720; ',
    'cookie1': 'BxUAdZcanV%2F0xYsoK9Y4JT9jlDALkfauJGPXoypV3f4%3D; ',
    'unb': '2750524052; ',
    'skt': '03f8b7c1716674d3; ',
    '_cc_': 'W5iHLLyFfA%3D%3D; ',
    '_l_g_': 'Ug%3D%3D; ',
    '_nk_': '%5Cu65E7%5Cu65F6%5Cu5149%5Cu7684%5Cu5E05%5Cu6C14%5Cu5C11%5Cu5E7420277; ',
    'cookie17': 'UU8NYS8hCF5h6g%3D%3D; ',
    'mt': 'ci=5_1; ',
    'alitrackid': 'www.taobao.com; ',
    'lastalitrackid': 'www.taobao.com; ',
    'JSESSIONID': '17001973B9E8A78C0F2CFE8B41D8B33A; ',
    'swfstore': '218055; ',
    'uc1': 'cart_m=0&cookie14=UoTdfYDVgrIDzA%3D%3D&lng=zh_CN&cookie16=UtASsssmPlP%2Ff1IHDsDaPRu%2BPw%3D%3D&existShop=false&cookie21=UtASsssme%2BBq&tag=8&cookie15=V32FPkk%2Fw0dUvg%3D%3D&pas=0; ',
    'isg': 'BCcnCmqkMVrz5rWVPwnmNd2ctlIxBPq9nFSWKfmVPrYd6FWqAn6b3wMiD-j2B9MG; ',
    'whl': '-1%260%260%261516549728835',
}

HEADERS = {
    'referer': 'https://www.taobao.com/?spm=a1z0d.6639537.0.0.77866266JWx96Z',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
}

# headers = {
#     'Host': 'www.zhihu.com',
#     'Referer': 'https://www.zhihu.com/api/v4/members/chi-wan-fan-la/followers?',
#     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'project.middlewares.ProjectSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'project.middlewares.ProjectDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'project.pipelines.ProjectPipeline': 300,
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
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
