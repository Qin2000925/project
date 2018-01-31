# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import time


class ZhiHutItem(scrapy.Item):
    answer_count = scrapy.Field()
    articles_count = scrapy.Field()
    follower_count = scrapy.Field()
    gender = scrapy.Field()
    headline = scrapy.Field()
    avatar_url = scrapy.Field()
    name = scrapy.Field()
    url_token = scrapy.Field()
    user_type = scrapy.Field()
    get_id = scrapy.Field()
    user_url = scrapy.Field()

    def get_mysql(self):
        t = int(time.time())
        time_local = time.localtime(t)
        t_a = time.strftime("%Y-%m-%d", time_local)

        sql_insert = "insert into zhi_hu_user(answer_count, articles_count, follower_count, gender, headline, " \
                     "avatar_url, name, url_token, user_type, get_id, user_url, add_time) VALUES " \
                     "('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
                     % (self['answer_count'], self['articles_count'], self['follower_count'], self['gender'],
                        self['headline'], self['avatar_url'], self['name'], self['url_token'], self['user_type'],
                        self['get_id'], self['user_url'], t_a)

        return sql_insert