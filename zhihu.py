import requests
import json
import re
import pymysql
import time
from urllib.parse import urlencode


class ZhiHu(object):
    def __init__(self):
        self.url = 'https://www.zhihu.com/api/v3/feed/topstory?'
        self.headers = {
            # 'ccept': 'application/json, text/plain, */*',
            # 'Accept-Encoding': 'gzip, deflate, br',
            # 'Accept-Language': 'zh-CN,zh;q=0.9',
            'authorization': 'Bearer 2|1:0|10:1515864976|4:z_c0|92:Mi4xdjhiYkJRQUFBQUFBWU9MN05NajdEQ1lBQUFCZ0FsVk5rSkZIV3dCc2xoV3AyX3VRZEJzQkpFR1hwNkFJeW96N0t3|a1fbaefdb1e15c2a821a9c3343ef225aba57c51bd549265cef941d3a34ef91a5',
            'Connection': 'keep-alive',
            'Cookie': '_zap=e071ca21-ed9c-4946-9763-5a82871f4d43; q_c1=6c2b5292a9744e86853d583a5a912370|1515490054000|1512308350000; aliyungf_tc=AQAAACaWJi/mhwEA5DMKcCbob5lOAOhR; d_c0="AGDi-zTI-wyPTpcX7Dz7JflHmp8fPit9oWU=|1515835238"; _xsrf=bc96ea5b-ce77-4ba4-b7fe-bd091cd83b53; capsion_ticket="2|1:0|10:1515864949|14:capsion_ticket|44:MDhlZWNkNzcwZDI0NGZhZDkyOWNjODM2MTg3YjUxNzY=|90b409c9c792d14057730e2f7bfe3d79bae7d12c96f7e8d69316461038a8ca82"; z_c0="2|1:0|10:1515864976|4:z_c0|92:Mi4xdjhiYkJRQUFBQUFBWU9MN05NajdEQ1lBQUFCZ0FsVk5rSkZIV3dCc2xoV3AyX3VRZEJzQkpFR1hwNkFJeW96N0t3|a1fbaefdb1e15c2a821a9c3343ef225aba57c51bd549265cef941d3a34ef91a5"',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
        }
        self.session = requests.session()
        self.page = 7

    def parse(self):
        while self.page <= 500:
            data = {
                'action_feed': 'True',
                'limit': '10',
                'session_token': '628cf1876431890b854e4be574d3b5b2',
                'action': 'down',
                'after_id': self.page,
                'desktop': 'true'
            }
            response = self.session.get(self.url + urlencode(data), headers=self.headers)
            response.encoding = 'utf-8'
            json_item = json.loads(response.text)
            print(json_item)

            connect = pymysql.connect(host='127.0.0.1', user='root', password='qinjiahu521', db='djangomysql', charset='utf8')
            cursor = connect.cursor()

            for item in json_item['data']:
                comment_count = item['target']['comment_count']
                target_id = item['target']['id']
                content = item['target']['content']
                get_content = ' '.join(re.findall('([\u4e00-\u9fa5]+)', content, re.S))
                target_type = item['target']['type']
                title = item['target']['question']['title']
                question_id = item['target']['question']['id']
                question_type = item['target']['question']['type']
                answer_count = item['target']['question']['answer_count']
                follower_count = item['target']['question']['follower_count']
                user_avatar_url = item['target']['author']['avatar_url']
                user_headline = item['target']['author']['headline']
                user_name = item['target']['author']['name']
                user_url_token = item['target']['author']['url_token']
                user_type = item['target']['author']['user_type']
                actors_name = item['actors'][0]['name']
                text_url = 'https://www.zhihu.com/' + str(question_type) + '/' + str(question_id) + '/' + str(target_type) + '/' + str(target_id)
                user_url = 'https://www.zhihu.com/{type}/{user}/activities'.format(type=user_type, user=user_url_token)

                t = int(time.time())
                time_local = time.localtime(t)
                dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
                try:
                    sql_insert = "insert into zhihu(title, text_url, user_url, actors_name, target_id, question_id, get_content, " \
                                 "target_type, question_type, answer_count, follower_count, user_avatar_url, user_headline, user_name, " \
                                 "user_url_token, user_type, comment_count, add_time) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', " \
                                 "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
                                 % (title, text_url, user_url, actors_name, target_id, question_id, get_content, target_type, question_type,
                                    answer_count, follower_count, user_avatar_url, user_headline, user_name,
                                    user_url_token, user_type, comment_count, dt)
                    cursor.execute(sql_insert)
                    connect.commit()
                    print('插入成功: ', sql_insert)
                except pymysql.err.DataError:
                    print(sql_insert)

            self.page += 8

if __name__ == '__main__':
    ZhiHu().parse()

