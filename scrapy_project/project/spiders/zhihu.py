# -*- coding: utf-8 -*-
import scrapy
import json
import time
from urllib.parse import urlencode
from project.items import *
from project.settings import *


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/']

    url = 'https://www.zhihu.com/api/v4/members/chi-wan-fan-la/followers?'
    page_url = 'https://www.zhihu.com/api/v4/members/{url_token}/followers?page={page}'
    user_url = 'https://www.zhihu.com/{user_type}/{user_token}/followers'
    page = 1
    offset = 0

    cookies = {'aliyungf_tc': 'AQAAAO2i2DfiFgAAgTMKcDOP3YORWXs8; ',
               'd_c0': '"AOBsEryMDw2PTpRRTu32ZzcLKZZ0RNjiVlM=|1517161825"; ',
               '_xsrf': 'f2754cb1-329d-4e5d-8a4d-8bfabcc269ec; ',
               'q_c1': '8ff5f220c4314b03be8dd4d7e8d56ef7|1517161825000|1517161825000; ',
               '_zap': 'b5b5cefb-1797-4d93-8294-d6312715b1dc; ',
               'capsion_ticket': '"2|1:0|10:1517161827|14:capsion_ticket|44:N2RlNDZiNTc3Yjg4NDI0YTk5NTczZjk0NzZjMGI1YzQ=|3eb8977f44ac9e5ed1ba8101df126fbd269e1c6110d0b0282656de4c3d39ee26"; ',
               'z_c0': '"2|1:0|10:1517161843|4:z_c0|92:Mi4xdjhiYkJRQUFBQUFBNEd3U3ZJd1BEU1lBQUFCZ0FsVk5jMXRiV3dDMmRzN3JvY1R4dFA0LXZkd094bkNubEhJZGtn|66d33389364f65c6387cf94d5a04be7b65d80a4aef7e5b01c0a29264387b1a82"'
            }
    zhi_hu_item = ZhiHutItem()

    def parse(self, response):
        data = {
            'include': 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics',
            'offset': self.offset,
            'limit': '20'
        }
        yield scrapy.Request(url=self.get_url(data), callback=self.parse_item, dont_filter=True,
                             cookies=self.cookies)

    def parse_item(self, response):
        try:
            json_response = json.loads(response.text)
            paging = json_response['paging']['is_end']
            next_url = json_response['paging']['next']
            item_data = json_response['data']
            for item in item_data:
                items, user_url = self.get_item(item)
                yield items
                # DEFAULT_REQUEST_HEADERS['Referer'] = user_url
                yield scrapy.Request(url=user_url, callback=self.parse_item, dont_filter=True,
                                     cookies=self.cookies)

            if paging == 'false' or not paging:
                self.page += 1
                # DEFAULT_REQUEST_HEADERS['Referer'] = self.page_url.format(url_token='', page=self.page)
                yield scrapy.Request(url=next_url, callback=self.parse_item, dont_filter=True,
                                     cookies=self.cookies)
        except Exception as e:
            print(response.status)
            print(response.url)
            print(response.text)
            print('error: ', e)
            time.sleep(1)

    def get_item(self, item):
        self.zhi_hu_item['answer_count'] = item['answer_count']
        self.zhi_hu_item['articles_count'] = item['articles_count']
        self.zhi_hu_item['follower_count'] = item['follower_count']
        self.zhi_hu_item['gender'] = '男' if str(item['gender']) == '1' else '女'
        self.zhi_hu_item['headline'] = item['headline']
        self.zhi_hu_item['avatar_url'] = item['avatar_url']
        self.zhi_hu_item['name'] = item['name']
        self.zhi_hu_item['url_token'] = item['url_token']
        self.zhi_hu_item['user_type'] = item['user_type']
        self.zhi_hu_item['get_id'] = item['id']
        self.zhi_hu_item['user_url'] = self.user_url.format(user_type=self.zhi_hu_item['user_type'],
                                                            user_token=self.zhi_hu_item['url_token'])

        return self.zhi_hu_item, self.zhi_hu_item['user_url']

    def get_url(self, data):
        return self.url + urlencode(data)