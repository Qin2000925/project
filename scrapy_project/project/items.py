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


class TaobaoprojectItem(scrapy.Item):
    nid = scrapy.Field()
    raw_title = scrapy.Field()
    pic_url = scrapy.Field()
    detail_url = scrapy.Field()
    view_price = scrapy.Field()
    view_fee = scrapy.Field()
    item_loc = scrapy.Field()
    view_sales = scrapy.Field()
    comment_count = scrapy.Field()
    user_id = scrapy.Field()
    nick = scrapy.Field()
    isTmall = scrapy.Field()

    def get_mysql(self):
        t = int(time.time())
        time_local = time.localtime(t)
        t_a = time.strftime("%Y-%m-%d", time_local)

        sql_insert = "insert into tao_bao_item(nid, raw_title, pic_url, detail_url, view_price, view_fee, item_loc, view_sales, " \
                     "comment_count, user_id, nick, isTmall, add_time) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s',  " \
                     "'%s', '%s', '%s', '%s', '%s', '%s')" \
                     % (self['nid'], self['raw_title'], self['pic_url'], self['detail_url'], self['view_price'], self['view_fee'],
                        self['item_loc'], self['view_sales'], self['comment_count'],
                        self['user_id'], self['nick'], self['isTmall'], t_a)

        return sql_insert