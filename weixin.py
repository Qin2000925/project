import requests
import lxml.html
from urllib.parse import urlencode
import re
import pymysql
import time
import random


class WeiXin(object):
    def __init__(self):
        self.url = 'http://weixin.sogou.com/weixin?'
        self.headers = {
            'Cookie': 'CXID=653258FF83BEEE3E454EE65CE463E543; SUID=A1320A705C68860A5A2516A100072C82; SMYUV=1512563768129497; IPLOC=CN3301; SUV=1516364235246332; ABTEST=8|1516364238|v1; weixinIndexVisited=1; ppinf=5|1516384896|1517594496|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToxODolRTclQTclQTYlRTUlQjAlOTF8Y3J0OjEwOjE1MTYzODQ4OTZ8cmVmbmljazoxODolRTclQTclQTYlRTUlQjAlOTF8dXNlcmlkOjQ0Om85dDJsdUlKdmotZWRNLW9kbGhXQkFiTTcza1FAd2VpeGluLnNvaHUuY29tfA; pprdig=bSljj1yQ23G9yK-wAgmZCqnPESSiHPhb5TQUHwZJC_jR_m9ULaHV6OiHazDnRdg5nK3GB8Rc89jps0DNT84i0Y6tFAJLQ_C29iP-WBqbCXYCsrhytOlSdo1xcX0NYsITahcYWPrhs4r4Rd41-88bQzbp0ec4v5HX67hviMxGyKM; sgid=03-30983589-AVpiaMoApMzOJpkMvM76p7jk; SUIR=A8505B21505432715E92577B51E8372B; ppmdig=151654868200000029b5cdfd8d54c9f7534f80b113a87ce1; PHPSESSID=d0ff429tq36v4g87seoe3384q2; sct=15; JSESSIONID=aaaGaSL_n8nNNeRUKJKdw; seccodeErrorCount=2|Sun, 21 Jan 2018 15:37:52 GMT; SNUID=99616B106164022A67AF37DE6171EF34; successCount=2|Sun, 21 Jan 2018 15:36:30 GMT',
            'Host': 'weixin.sogou.com',
            'Referer': 'http://weixin.sogou.com/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
        }

        self.session = requests.session()
        self.page = 1

        self.connect = pymysql.connect(host='127.0.0.1', user='root', password='qinjiahu521', db='python', charset='utf8')
        self.cursor = self.connect.cursor()

    def proxy(self):
        while True:
            try:
                headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}
                url = 'http://127.0.0.1:5000/get'
                res = requests.get(url).text.strip()
                proxies = {"http": "http://" + res}
                response = requests.get('https://www.baidu.com/', headers=headers)
                if response.status_code == 200:
                    print('Valid proxy: ', proxies)
                    return proxies
                print('Invalid proxy: ', proxies)
            except Exception as e:
                print('出现异常: ', e)

    def parse(self):
        name = ['python', 'java', 'php', 'c++']
        for i in name:
            print(i)
            a = 1
            while self.page < 100:
                if a >= 500:
                    print('错误出现--%d--次退出程序' % a)
                    break
                data = {
                    'query': i,
                    '_sug_type_': '',
                    's_from': 'input',
                    '_sug_': 'n',
                    'type': '2',
                    'page': self.page,
                    'ie': 'utf8',
                }
                if self.headers['Referer'] != 'http://weixin.sogou.com/':
                    self.headers['Referer'] = self.url+ urlencode(data)
                try:
                    # proxies = self.proxy()  proxies=proxies,
                    # print('Obtain proxy success', proxies)
                    response = self.session.get(self.url+ urlencode(data), headers=self.headers, timeout=5)
                    get_html = lxml.html.fromstring(response.text)
                    url = get_html.xpath('//*[@class="news-list"]/li/div[2]/h3/a/@href')

                    for i in url:
                        t = int(time.time())
                        sql_insert = "insert into weixin(url, get_keys) VALUES ('%s', '%s')" % (i.replace('\'', ''), str(t))
                        self.cursor.execute(sql_insert)
                        self.connect.commit()
                        print('success-11111')
                        self.item(i, t)
                        self.page += 1
                except Exception as e:
                    print('error 错误--%d--次' % a, e)
                    a += 1
            if a >= 500:
                break

    def item(self, url, t):
        time.sleep(random.randint(3, 5) / 2)
        print(url)
        headers = {
            'Host': 'mp.weixin.qq.com',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
        }
        sql_insert = ''
        try:
            response = self.session.get(url, headers=headers)
            get_html = lxml.html.fromstring(response.text)

            title = re.findall('<h2 class="rich_media_title" id="activity-name">\s(.*?)\s</h2>', response.text, re.S)
            times = re.findall('<em id="post-date" class="rich_media_meta rich_media_meta_text">(.*?)</em>', response.text)
            name = re.findall('<a class=".*?" href="##" id="post-user">(.*?)</a>', response.text)
            connect = get_html.xpath('//*[@id="js_content"]/p/text() | //*[@id="js_content"]/p/span/text()')
            images = get_html.xpath('//*[@id="js_content"]/p/img/@data-src')
            read = get_html.xpath('//*[@id="js_sg_bar"]/a/text()')
            read_url = get_html.xpath('//*[@id="js_sg_bar"]/a/@href')

            sql_insert = "insert into weixin_title(title, connect, times, name, get_read, get_read_url, get_keys) " \
                         "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
                         % (''.join(title).strip().replace('\'', ''), ' '.join(connect).strip().replace('\'', ''),
                            ''.join(times).strip().replace('\'', ''), ''.join(name).strip().replace('\'', ''),
                            ''.join(read).strip().replace('\'', ''), ''.join(read_url).strip().replace('\'', ''), str(t))
            self.cursor.execute(sql_insert)
            self.connect.commit()
            print('success-22222')
            self.get_images(images, t)

        except Exception as e:
            print('sql_insert: ', sql_insert, e)

    def get_images(self, images, t):
        time.sleep(random.randint(3, 5) / 2)
        if images:
            for i in images:
                print(i)
                sql_insert = ''
                try:
                    sql_insert = "insert into weixin_images(get_keys, images) VALUES " \
                                 "('%s', '%s')" % (t, i)
                    self.cursor.execute(sql_insert)
                    self.connect.commit()
                    print('success-33333')
                except Exception as e:
                    print('sql_insert: ', sql_insert, e)


if __name__ == '__main__':
    WeiXin().parse()