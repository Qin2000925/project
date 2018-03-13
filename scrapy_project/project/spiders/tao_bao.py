# -*- coding: utf-8 -*-
import scrapy
import json
import re
from ..settings import COOKIES, HEADERS

from ..items import *
import time
import random


class TaoBaoSpider(scrapy.Spider):
    name = 'tao_bao'
    allowed_domains = ['taobao.com']
    start_urls = ['https://www.taobao.com/']

    tao_bao_item = TaobaoprojectItem()

    def parse(self, response):
        url = 'https://s.taobao.com/search?initiative_id=tbindexz_20170306&ie=utf8&spm=a21bo.2017.201856-taobao-item.2&' \
              'sourceId=tb.index&search_type=item&ssid=s5-e&commend=all&imgfile=&q=%E7%94%B7%E5%A3%AB%E5%A4%96%E5%A5%97&' \
              'suggest=history_1&_input_charset=utf-8&wq=&suggest_query=&source=suggest'
        yield scrapy.Request(url=url, callback=self.parse_item, dont_filter=True, headers=HEADERS)

    def parse_item(self, response):
        # n = 1
        # a = 1
        # if response.status != 302 and response.status == 200:
        #     while True:
        #         try:
        #             if n > 100:
        #                 print('error appear 100 second --- Exit procedure')
        #                 break
        html = re.findall('g_page_config = (.*?)g_srp_loadCss\(\);', response.text, re.S)
        json_item = json.loads(html[0].strip()[:-1])['mods']['itemlist']['data']['auctions']
        print(json_item)
        for items in json_item:
            self.item_data(items)
            yield self.tao_bao_item

        if len(json_item) == 36:
            HEADERS['referer'] = response.url
            time.sleep(random.randint(3, 5) / 2)
            yield scrapy.Request(url=tao_bao(), dont_filter=True, callback=self.parse_item_page, headers=HEADERS)
        #         except Exception as e:
        #             print('one response: ', response.status)
        #             n += 1
        #             print('error: %d ' % n, e)
        # else:
        #     if a > 50:
        #         print('error appear 50 second --- Exit procedure')
        #         return False
        #     a += 1
        #     url = 'https://s.taobao.com/search?initiative_id=tbindexz_20170306&ie=utf8&spm=a21bo.2017.201856-taobao-item.2&' \
        #           'sourceId=tb.index&search_type=item&ssid=s5-e&commend=all&imgfile=&q=%E7%94%B7%E5%A3%AB%E5%A4%96%E5%A5%97&' \
        #           'suggest=history_1&_input_charset=utf-8&wq=&suggest_query=&source=suggest'
        #     yield scrapy.Request(url=url, callback=self.parse_item, dont_filter=True, cookies=COOKIES, headers=HEADERS)

    def parse_item_page(self, response):
        item = re.findall('jsonp\d+\((.*?)\);', response.text, re.S)[0]
        json_item = json.loads(item)['API.CustomizedApi']['itemlist']['auctions']

        for items in json_item:
            self.item_data(items)
            yield self.tao_bao_item
        #
        # n = 1
        # while True:
        #     try:
        #         if n > 100:
        #             print('one error appear 100 second --- Exit procedure')
        #             break
        for num in range(1, 500):
            url = tao_bao_conf(num * 44, (num - 1) * 44)
            if num != 1:
                HEADERS['referer'] = url
            time.sleep(random.randint(3, 5) / 2)
            yield scrapy.Request(url=url, dont_filter=True, callback=self.tao_bao_text_page, headers=HEADERS)
            # except Exception as e:
            #     print('response: ', response.status)
            #     n += 1
            #     print('error: %d ' % n, e)

    def tao_bao_text_page(self, response):
        try:
            item = re.findall('jsonp\d+\((.*?false}})\);', response.text.strip(), re.S)[0]
            json_item = json.loads(item)['mods']['itemlist']['data']['auctions']
            print(json_item)
            for items in json_item:
                self.item_data(items)
                yield self.tao_bao_item
        except Exception as e:
            print(response.text.strip())
            print(response.status)

    def item_data(self, items):
        try:
            self.tao_bao_item['nid'] = items['nid']
            self.tao_bao_item['raw_title'] = items['raw_title'].strip()
            self.tao_bao_item['pic_url'] = items['pic_url'].strip() if 'https:' in items['pic_url'] else 'https:' + items['pic_url']
            self.tao_bao_item['detail_url'] = items['detail_url'].strip() if 'https:' in items['detail_url'] else 'https:' + items['detail_url']
            self.tao_bao_item['view_price'] = items['view_price'].strip()
            self.tao_bao_item['view_fee'] = 'no' if float(items['view_fee']) else 'yes'
            self.tao_bao_item['item_loc'] = items['item_loc'].strip()
            self.tao_bao_item['view_sales'] = items['view_sales'].strip()
            self.tao_bao_item['comment_count'] = items['comment_count']
            self.tao_bao_item['user_id'] = items['user_id']
            self.tao_bao_item['nick'] = items['nick']
            self.tao_bao_item['isTmall'] = 'yes' if items['shopcard']['isTmall'] else 'no'
            return True
        except Exception as e:
            print(e)
            return False
