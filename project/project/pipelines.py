# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from project.settings import *


class ProjectPipeline(object):
    def process_item(self, item, spider):
        connect = pymysql.connect(host=MYSQL_HOST, password=MYSQL_PASSWORD, db=MYSQL_DB, user=MYSQL_USER,
                                  charset='utf8')
        cursor = connect.cursor()
        sql_insert = ''
        try:
            sql_insert = item.get_mysql()
            cursor.execute(sql_insert)
            connect.commit()
            print('success: ', sql_insert)
        except pymysql.IntegrityError:
            print('error: ', sql_insert)
        return item
