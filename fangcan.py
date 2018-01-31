import requests
import lxml.html
import time
import pymysql


class ESFang(object):
    def __init__(self):
        self.url = 'https://hangzhou.anjuke.com/sale/jianggan/p%d-rd1/'

        self.headers = {
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
        }
        self.session = requests.session()
        self.page = 1

        self.connect = pymysql.connect(host='127.0.0.1', user='root', password='qinjiahu521', db='djangomysql', charset='utf8')
        self.cursor = self.connect.cursor()

    def parse(self):
        while self.page < 50:
            if self.page == 1:
                self.headers['referer'] = 'https://hangzhou.anjuke.com/sale/jianggan/rd1/'
            elif self.page > 1:
                self.headers['referer'] = self.url
            response = self.session.get(self.url % self.page, headers=self.headers)
            get_html = lxml.html.fromstring(response.text)
            item_img = get_html.xpath('//*[@id="houselist-mod-new"]/li/div[1]/img/@src')
            item_title = get_html.xpath('//*[@id="houselist-mod-new"]/li/div[2]/div[1]/a/@title')
            item_url = get_html.xpath('//*[@id="houselist-mod-new"]/li/div[2]/div[1]/a/@href')
            item_info1 = get_html.xpath('//*[@id="houselist-mod-new"]/li/div[2]/div[2]/span[1]/text()')
            item_info2 = get_html.xpath('//*[@id="houselist-mod-new"]/li/div[2]/div[2]/span[2]/text()')
            item_info3 = get_html.xpath('//*[@id="houselist-mod-new"]/li/div[2]/div[2]/span[3]/text()')
            item_info4 = get_html.xpath('//*[@id="houselist-mod-new"]/li/div[2]/div[2]/span[4]/text()')
            item_info5 = get_html.xpath('//*[@id="houselist-mod-new"]/li/div[2]/div[2]/span[5]/text()')
            item_address = get_html.xpath('//*[@id="houselist-mod-new"]/li/div[2]/div[3]/span/@title')
            item_price1 = get_html.xpath('//*[@id="houselist-mod-new"]/li/div[3]/span[1]/strong/text()')
            item_price2 = get_html.xpath('//*[@id="houselist-mod-new"]/li/div[3]/span[2]/text()')
            for i in zip(item_img, item_title, item_url, item_info1, item_info2, item_info3, item_info4,
                         item_info5, item_address, item_price1, item_price2):
                t = int(time.time())
                time_local = time.localtime(t)
                dt = time.strftime("%Y-%m-%d", time_local)

                sql_insert = "insert into fangcan(item_img, item_title, item_url, item_info1, item_info2, item_info3, " \
                             "item_info4, item_info5, item_address, item_price1, item_price2, add_time) " \
                             "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
                             % (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7],
                                i[8].replace('\xa0\xa0', '').strip(), i[9], i[10], dt)
                self.cursor.execute(sql_insert)
                self.connect.commit()
                print('插入成功: ', sql_insert)
            time.sleep(2)
            self.page += 1


if __name__ == '__main__':
    # ESFang().parse()
    connect = pymysql.connect(host='127.0.0.1', user='root', password='qinjiahu521', db='djangomysql', charset='utf8')
    cursor = connect.cursor()

    cursor.execute('select * from fangcan')
    item = cursor.fetchall()
    for i in item:
        print(i[5])