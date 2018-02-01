import requests
import time
import pymysql
import re
import json
import random


class BiliUserInfo(object):
    def __init__(self):
        self.user_info = 'https://space.bilibili.com/ajax/member/GetInfo'
        self.followers = 'https://api.bilibili.com/x/relation/followers?vmid={user_id}&pn={pn}&' \
                         'ps=20&order=desc&jsonp=jsonp&callback=__jp{callback_num}'  # &callback=__jp{callback_num}
        self.relation = 'https://api.bilibili.com/x/relation/stat?vmid={user_id}&jsonp=jsonp&callback=__jp3'

        self.headers = {
            # 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
            # 'Cookie': 'finger=49387dad; LIVE_BUVID=AUTO1615173955999667; sid=bmhc63jg; buvid3=04F0AF21-D446-46F7-979E-85E371EFE8217039infoc; UM_distinctid=1614bd3b7e93e-0175557e4934bb-1e291c08-100200-1614bd3b7ea1dd; fts=1517395622; pgv_pvi=5466716160; rpdid=oqmlmoxmkmdosomklsxiw; DedeUserID=284956450; DedeUserID__ckMd5=310b93bd3670d213; SESSDATA=845742cd%2C1517480397%2C179324a2; bili_jct=11f56e1d7da573330f9f6e0b9e8afb09; _dfcaptcha=90fd9df7c60da89d3904afc4e7a7d4f5; purl_token=bilibili_1517475085; pgv_si=s2833464320; CNZZDATA2724999=cnzz_eid%3D1393768691-1517392378-https%253A%252F%252Fwww.bilibili.com%252F%26ntime%3D1517473381',
            'X-Requested-With': 'XMLHttpRequest'
        }
        self.session = requests.session()
        self.callback_num = 10

        self.connect = pymysql.connect(host='127.0.0.1', user='root', db='python', password='qinjiahu521', charset='utf8')
        self.cursor = self.connect.cursor()
        self.ua_list = self.get_ua()

    def parse(self, user_id):
        for get_id in user_id: # https://space.bilibili.com/13234163?spm_id_from=333.338.common_report.6
            response = ''
            try:
                self.headers['Referer'] = 'https://space.bilibili.com/{user_id}?spm_id_from=333.338.common_report.6'.format(user_id=get_id)
                self.headers['User-Agent'] = random.choice(self.ua_list)
                data = {
                    'mid': get_id,
                    'csrf': '11f56e1d7da573330f9f6e0b9e8afb09'
                }
                proxies = self.get_proxy()
                print('Obtain proxy success ont', proxies)
                response = self.session.post(url=self.user_info, data=data, headers=self.headers, proxies=proxies).json()
                print(response)
                status_json = response['status'] if 'status' in response.keys() else False
                if status_json:
                    json_item = response['data']
                    if json_item:
                        sign = json_item['sign']
                        mid= json_item['mid']
                        name = json_item['name']
                        place = json_item['place']
                        sex = json_item['sex']
                        coins = json_item['coins']
                        birthday = json_item['birthday']
                        description = json_item['description']
                        article = json_item['article']
                        playNum = json_item['playNum']
                        reg_time = json_item['regtime']
                        current_level = json_item['level_info']['current_level']
                        current_exp = json_item['level_info']['current_exp']
                        spaces_ta = json_item['spacesta']
                        face = json_item['face']

                        time.sleep(1)
                        start_res = self.session.get(self.relation.format(user_id=mid), headers=self.headers)
                        start_res = re.findall('__jp\d+\((.*?)\)', start_res.text)
                        start_res = json.loads(start_res[0])
                        follower = start_res['data']['follower']
                        following = start_res['data']['following']

                        sql_insert = ''
                        reg_time = self.get_time(t=reg_time)

                        t = time.time()
                        time_local = time.localtime(int(t))
                        dt = time.strftime("%Y-%m-%d", time_local)
                        try:
                            sql_insert = "insert into bili_user_info(mid, name, sex, place, sign, follower, following, birthday, reg_time, playNum, " \
                                         "coins, description, article, current_level, current_exp, spaces_ta, face, add_time) " \
                                         "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', " \
                                         "'%s', '%s', '%s')" \
                                         % (mid, name, sex, place, sign, follower, following, birthday, str(reg_time), playNum, coins,
                                            description, article, current_level, current_exp, spaces_ta, face, dt)
                            self.cursor.execute(sql_insert)
                            self.connect.commit()
                            print('SUCCESS SQL', sql_insert)
                            # self.followers_list(get_id)
                        except Exception as e:
                            print('SQL ERROR',sql_insert, e)
                        self.followers_list(get_id)
                else:
                    print(response)
                    print('response error time sleep too second again request')
                    time.sleep(2)
                    self.parse([random.randint(100000000, 500000000)])
            except ValueError as e:
                print(response)
                print('ValueError time sleep too second again request', e)
                time.sleep(2)
                self.parse([random.randint(100000000, 500000000)])

    def followers_list(self, user_id):
        pn = 1
        callback_num = 10
        while pn < 5:
            response = ''
            try:
                self.headers[
                    'Referer'] = 'https://space.bilibili.com/{user_id}?spm_id_from=333.338.common_report.6'.format(
                    user_id=user_id)
                time.sleep(2)
                proxies = self.get_proxy()
                print('Obtain proxy success too', proxies)
                response = self.session.get(self.followers.format(user_id=user_id, pn=pn, callback_num=callback_num),
                                            headers=self.headers, proxies=proxies)
                print(response.text)
                response = re.findall('__jp\d+\((.*?)\)', response.text)
                json_item = json.loads(response[0])
                mid_list = []
                json_data = json_item['data']['list']
                if json_data:
                    for mid in json_data:
                        mid = mid['mid']
                        mid_list.append(mid)
                        self.parse([mid])
                    pn += 1
                    callback_num += 1
                    # self.parse(mid_list)
                else:
                    self.parse([random.randint(100000000, 500000000)])
            except Exception as e:
                print(response)
                print('error time sleep too second --> ', e)
                time.sleep(2)
            self.parse([random.randint(100000000, 500000000)])

    def get_time(self, t=time.time()):
        try:
            time_local = time.localtime(int(t))
            dt = time.strftime("%Y-%m-%d", time_local)
            return dt
        except Exception as e:
            print('time error', e)
            return ''

    def get_proxy(self):
        while True:
            try:
                response = requests.get('http://api.ip.data5u.com/dynamic/get.html?order=e21ad37b142f45945d7c7b090fa59197&sep=3')
                proxies = {'http': 'http://' + response.text.strip()}
                headers = {
                    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}
                res = requests.get('https://www.baidu.com/', proxies=proxies, headers=headers)
                if res.status_code == 200:
                    print('Valid proxy: ', proxies)
                    return proxies
                print('Invalid proxy: ', proxies)
            except Exception as e:
                print('proxy error', e)

    def get_ua(self):
        with open('ua', mode='r') as f:
            ua_list = []
            for ua in f.readlines():
                ua_list.append(ua.strip()[1:-1])
            return ua_list

    def create_mysql(self):
        """mid, name, sex, place, sign, follower, following, birthday, reg_time, playNum,
           coins, description, article, current_level, current_exp, spaces_ta, face, add_time"""
        sql = "create table bili_user_info (" \
              "mid INT PRIMARY KEY NOT NULL, " \
              "name VARCHAR(100), " \
              "sex VARCHAR(10), " \
              "place VARCHAR(50), " \
              "sign VARCHAR (500), " \
              "follower VARCHAR(50), " \
              "following VARCHAR(50), " \
              "birthday VARCHAR(50), " \
              "reg_time VARCHAR(50), " \
              "playNum VARCHAR(20), " \
              "coins VARCHAR(20), " \
              "description VARCHAR(500), " \
              "article VARCHAR(50), " \
              "current_level VARCHAR(50), " \
              "current_exp VARCHAR(50), " \
              "spaces_ta VARCHAR(50), " \
              "face VARCHAR(300), " \
              "add_time datetime)"
        self.cursor.execute(sql)
        self.connect.commit()
        self.parse(21056945)


if __name__ == '__main__':
    BiliUserInfo().parse([random.randint(100000000, 500000000)])
    # BiliUserInfo().get_proxy()
    # BiliUserInfo().get_ua()
