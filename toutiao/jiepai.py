import requests
import pymysql
import time


class JeiPai(object):
    def __init__(self):
        self.image_url = 'https://www.toutiao.com/search_content/?'
        self.headers = {
            'referer': 'https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }
        self.session = requests.session()
        self.offset = 0

        self.connect = pymysql.connect(host='127.0.0.1', db='python', user='root', password='qinjiahu521', charset='utf8')
        self.cursor = self.connect.cursor()

    def parse(self):
        while self.offset < 1000:
            data = {
                'offset': self.offset,
                'format': 'json',
                'keyword': '街拍',
                'autoload': 'true',
                'count': '20',
                'cur_tab': '3',
                'from': 'gallery'
            }
            response = self.session.get(self.image_url, params=data, headers=self.headers).json()['data']
            for item in response:
                article_url = item['article_url']
                create_time = item['create_time']
                display_time = item['display_time']
                date_time = item['datetime']
                comment_count = item['comment_count']
                title = item['title']
                media_name = item['media_name']
                media_url = item['media_url']
                media_creator_id = item['media_creator_id']
                group_id = item['group_id']
                image_detail = item['image_detail']

                sql_insert = ''
                try:
                    sql_insert = "insert into jie_pai(user_id, user_name, title, title_url, user_url, title_id, comment_count, " \
                                 "create_time, display_time, date_time, add_time) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', " \
                                 "'%s', '%s', '%s', '%s', '%s')" \
                                 % (media_creator_id, media_name, title, article_url, media_url, group_id,
                                    comment_count, self.times(create_time), self.times(display_time),date_time,self.times())
                    self.cursor.execute(sql_insert)
                    self.connect.commit()
                    print('SUCCESS MYSQL:', sql_insert)
                    self.image(image_detail, group_id)
                    time.sleep(2)

                except Exception as e:
                    print('MYSQL ERROR:', e, sql_insert)
                    time.sleep(2)
            self.offset += 20

    def image(self, image_list, group_id):
        for image in image_list:
            image__url = image['url_list']
            image_id = image['uri']
            sql_insert = ''
            try:
                sql_insert = "insert into image_list(user_id, image_id, image_url) VALUES ('%s', '%s', '%s')" \
                             % (group_id, image_id, image__url)
                self.cursor.execute(sql_insert)
                self.connect.commit()
                print('IMAGE SUCCESS MYSQL:', sql_insert)

            except Exception as e:
                print(image_list)
                print('IMAGE MYSQL ERROR:', e, sql_insert)
                return False
        return True

    def times(self, get_time=time.time()):
        try:
            time_local = time.localtime(int(get_time))
            dt = time.strftime("%Y-%m-%d", time_local)
            return dt
        except Exception as e:
            print('time error', e)
            return ''

    def create_mysql(self):
        sql = "create table jie_pai (" \
              "title_id VARCHAR (30) PRIMARY KEY NOT NULL , " \
              "user_name VARCHAR (50), " \
              "title VARCHAR (100), " \
              "title_url VARCHAR (300), " \
              "user_url VARCHAR (300), " \
              "user_id INT, " \
              "comment_count INT , " \
              "create_time datetime, " \
              "display_time datetime, " \
              "date_time VARCHAR (30), " \
              "add_time datetime)"

        image_sql = "create table image_list(" \
                    "title_id VARCHAR (30), " \
                    "image_id VARCHAR (30) PRIMARY KEY NOT NULL , " \
                    "image_url VARCHAR (300))"
        self.cursor.execute(sql)
        self.cursor.execute(image_sql)
        self.connect.commit()


if __name__ == '__main__':
    JeiPai().parse()
    # a = [{'url': 'http://p3.pstatp.com/large/5e7c0005361a1eec64bc', 'width': 959, 'url_list': [{'url': 'http://p3.pstatp.com/large/5e7c0005361a1eec64bc'}, {'url': 'http://pb9.pstatp.com/large/5e7c0005361a1eec64bc'}, {'url': 'http://pb1.pstatp.com/large/5e7c0005361a1eec64bc'}], 'uri': 'large/5e7c0005361a1eec64bc', 'height': 1440}, {'url': 'http://p3.pstatp.com/large/5e7a0005caef0f2dee12', 'width': 960, 'url_list': [{'url': 'http://p3.pstatp.com/large/5e7a0005caef0f2dee12'}, {'url': 'http://pb9.pstatp.com/large/5e7a0005caef0f2dee12'}, {'url': 'http://pb1.pstatp.com/large/5e7a0005caef0f2dee12'}], 'uri': 'large/5e7a0005caef0f2dee12', 'height': 1487}, {'url': 'http://p1.pstatp.com/large/5e8100037813ea39e172', 'width': 960, 'url_list': [{'url': 'http://p1.pstatp.com/large/5e8100037813ea39e172'}, {'url': 'http://pb3.pstatp.com/large/5e8100037813ea39e172'}, {'url': 'http://pb9.pstatp.com/large/5e8100037813ea39e172'}], 'uri': 'large/5e8100037813ea39e172', 'height': 1703}, {'url': 'http://p1.pstatp.com/large/5e8300037ffae4a7addd', 'width': 1632, 'url_list': [{'url': 'http://p1.pstatp.com/large/5e8300037ffae4a7addd'}, {'url': 'http://pb3.pstatp.com/large/5e8300037ffae4a7addd'}, {'url': 'http://pb9.pstatp.com/large/5e8300037ffae4a7addd'}], 'uri': 'large/5e8300037ffae4a7addd', 'height': 2449}, {'url': 'http://p3.pstatp.com/large/5e7c00053d467dacbc6f', 'width': 1502, 'url_list': [{'url': 'http://p3.pstatp.com/large/5e7c00053d467dacbc6f'}, {'url': 'http://pb9.pstatp.com/large/5e7c00053d467dacbc6f'}, {'url': 'http://pb1.pstatp.com/large/5e7c00053d467dacbc6f'}], 'uri': 'large/5e7c00053d467dacbc6f', 'height': 2661}, {'url': 'http://p1.pstatp.com/large/5e7a0005d7d222e0145e', 'width': 1612, 'url_list': [{'url': 'http://p1.pstatp.com/large/5e7a0005d7d222e0145e'}, {'url': 'http://pb3.pstatp.com/large/5e7a0005d7d222e0145e'}, {'url': 'http://pb9.pstatp.com/large/5e7a0005d7d222e0145e'}], 'uri': 'large/5e7a0005d7d222e0145e', 'height': 2479}, {'url': 'http://p9.pstatp.com/large/5e7b0005a9cd12ea0ce7', 'width': 1599, 'url_list': [{'url': 'http://p9.pstatp.com/large/5e7b0005a9cd12ea0ce7'}, {'url': 'http://pb1.pstatp.com/large/5e7b0005a9cd12ea0ce7'}, {'url': 'http://pb3.pstatp.com/large/5e7b0005a9cd12ea0ce7'}], 'uri': 'large/5e7b0005a9cd12ea0ce7', 'height': 2501}]
    # for i in a:
    #     print(i['url'], i['uri'])