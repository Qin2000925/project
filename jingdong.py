import requests
from urllib.parse import urlencode
import lxml.html
import json
import pymysql
import time
import multiprocessing
import threading


class JingDong(object):
    def __init__(self):
        self.url = 'https://search.jd.com/Search?'

        self.comment_url = 'https://sclub.jd.com/comment/productPageComments.action?'

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
            'Cookie': '__jdu=1492061309; xtest=803.cf6b6759; PCSYCityID=1213; qrsc=3; mt_xid=V2_52007VwMXWl5ZVVodSBFsVjULGlQPXVVGGx4ZXRliAxMAQQtWD09VH1sCZVQUUV1cBQ0WeRpdBW4fE1JBWFFLHEkSXA1sABFiX2hSah9PGFkCZAYRUW1YV1wY; user-key=84d76d67-471e-4b4e-b90f-4b0c62d6ca5f; _pst=jd_5af70cb63f584; logintype=qq; unick=jd_5af70cb63f584; pin=jd_5af70cb63f584; npin=jd_5af70cb63f584; _tp=%2FCsu1pW05Pc935pWAnxw%2B6ifopyYV78MI2KWpPPn1Zo%3D; ipLocation=%u6d59%u6c5f; areaId=15; ipLoc-djd=15-1213-1214-50142.138584065; cn=0; __utma=122270672.544021720.1515764223.1515764223.1515764223.1; __utmz=122270672.1515764223.1.1.utmcsr=trade.jd.com|utmccn=(referral)|utmcmd=referral|utmcct=/shopping/order/getOrderInfo.action; __jdv=122270672|direct|-|none|-|1515919457135; unpl=V2_ZzNtbUBRQBEnWhUEchwLBWJXQQ5LVkEXdAEUV3xLC1BjARZZclRCFXwUR1RnGVkUZAEZXUZcQxBFCHZXchBYAWcCGllyBBNNIEwHDCRSBUE3XHxcFVUWF3RaTwEoSVoAYwtBDkZUFBYhW0IAKElVVTUFR21yVEMldQl2VH4RXwRgAxBcSmdzEkU4dlFyGlUBVwIiXHIVF0l8CU5TfhwRBWILEVxFV0EUfThHZHg%3d; CCC_SE=ADC_9sGUMK1mgSGcHZiTrj2fEvS%2bmi%2bUuNtbE%2bOFryhlLCc%2blAFzDX5KSCBoWu1qSwhaqFka%2fRGIsDsssSEM1%2flOYpe%2fyh4eAKmhNG42NAwqfnPvhQ9Dxa5huhX4RaEH5BMmygeTWLiGztLLTGpcHZlRb2RveAgza8G2zlLTBa5XLe90gR4ckY0YECLfmTA5ub6z4lWeRNPyzT9xw%2bVBLRgBI0BOeVcYZAEpmDzpo1gkOVeDHdvOd%2bYsk54rCYbe6L7eC6YW8c8o4PbkIMprFBw74mfJW6gvAfJXtnj2K8ypqSpYFj58aCwN3Bl51xrjg0FEbGUgBK7v3GjHV%2bKxOxmOeIlnqKkbiTWDalPIRccfkH%2fAtkwXM2ZoKrpE6s0p%2fSKnesFPmdwG9tg6%2b%2fEJnovyeR6tFMB0GgYkTBTkGHpPCGiMVDJt8cnpesFgNy%2bk5696%2fCmXIHFy7PBwYFiy0n0irvROa6fF1gECut7v5lbS7Kteo59j3tq1zOLva7h36fAo8QM%2b3kuf%2b6D%2bjqZWOOq%2bqiPJH3KRgJ2SHBy%2b226gS1YKYWoxwRvTg%2byJcyyIsRkq30pr0749151pPNz1kwVNThkRav%2bkQqPZnz6ggYw59R%2fjPBBPHEgc0Wvd72gOKIjH8wh7la2cSpu0Mnsnm%2fJJh1VF4Qx%2bcX1QpqLQFFuVU%2fWqFWFwEkI%2bD6BdGY7nFdRIKS%2bEERW09ZYDHUOiMDddEXR%2bg8bp1wC4yWLXTh6Q%2bLs%3d; __jda=122270672.1492061309.1512304456.1515919457.1515942915.5; __jdc=122270672; rkv=V0200; _jrda=3; _jrdb=1515946406545; wlfstk_smdl=bwuxhhzk050yt5p02rdtvi3rax81epgp; thor=08A615E49F34EE42C9A52BFCF2B2E2DA36A3516F97A8C31ACEC8C597931939BF61187B0F87C458E3DE098F7A6AC8D1BAA4CF755ECCF40A27027B1AEB798BB0A0B8083FAD66A35A49C76DB46428F2DE296BF87F3EA3D1B19D50413AE9EEFBBEFC98FF5964405243A681ADA81DB1956298905FE09DE50F86EECE7F1C4B6D1B8068544807E05190DECB7074C955EB4BF21B5A018F3149E813B10DAD173F0C9904CA; pinId=Vjtiu_aYDCD51ISrWJeQ-rV9-x-f3wj7; __jdb=122270672.26.1492061309|5.1515942915; 3AB9D23F7A4B3C9B=FJJAMSAWXQQDVY6NFZOKNZYWHZCKRT7ZHF3ES4SWBGQM6A3HRUGMZU4G7I4LY3E5K5UBGJSLVUBZCFQ25Q4LLHKJGQ'
        }
        self.session = requests.session()
        self.page = 1

        self.connect = pymysql.connect(host='127.0.0.1', user='root', password='qinjiahu521', db='djangomysql', charset='utf8')
        self.cursor = self.connect.cursor()

    def parse(self):
        while self.page < 100:
            data = {
                'keyword': '外套男冬季',
                'enc': 'utf-8',
                'qrst': '1',
                'rt': '1',
                'stop': '1',
                'vt': '2,',
                'page': self.page,
                'scrolling': 'y',
                'log_id': '1515943811.13720',
                'tpl': '3_L'
            }
            response = self.session.get(self.url + urlencode(data), headers=self.headers)
            response.encoding = 'utf-8'
            item = lxml.html.fromstring(response.text)

            data_pid = item.xpath('//*[@class="gl-warp clearfix"]/li/@data-pid')
            image = item.xpath('//*[@class="gl-warp clearfix"]/li/div/div[1]/a/img/@src')
            price = item.xpath('//*[@class="gl-warp clearfix"]/li/div/div[3]/strong/i/text()')
            comment_count = item.xpath('//*[@class="gl-warp clearfix"]/li/div/div[5]/strong/a/text()')
            name = item.xpath('//*[@class="gl-warp clearfix"]/li/div/div[7]/span/a/text()')
            name_url = item.xpath('//*[@class="gl-warp clearfix"]/li/div/div[7]/span/a/@href')
            get_id = []
            a = 1
            for item in zip(data_pid, image, price, comment_count, name, name_url):
                t = int(time.time())
                time_local = time.localtime(t)
                dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
                sql_insert = ''
                try:
                    sql_insert = "insert into jingdong(data_pid, image, price, comment_count, name, name_url, add_time) VALUES " \
                                 "('%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
                                 % (item[0], item[1], item[2], item[3], item[4], item[5], dt)
                    self.cursor.execute(sql_insert)
                    self.connect.commit()
                    print('插入成功: ', sql_insert)
                    print('a-----%d' % a)
                    a += 1
                    get_id.append(item[0])
                except Exception as e:
                    print('error: ', sql_insert, e)
            t1 = threading.Thread(target=self.comment, args=(get_id,))
            t1.start()
            self.page += 1
            # self.comment(item[0])

    def comment(self, id_list):
        comment_page = 0
        for id in id_list:
            while True:
                data = {
                    'productId': id,
                    'score': '0',
                    'sortType': '5',
                    'page': comment_page,
                    'pageSize': '10',
                    'isShadowSku': '0',
                    'rid': '0',
                    'fold': '1'
                }
                response = self.session.get(self.comment_url + urlencode(data), headers=self.headers)

                item_json = json.loads(response.text)
                comment_max_page = item_json['maxPage']
                b = 1
                for item in item_json['comments']:
                    anonymousFlag = item['anonymousFlag']
                    content = item['content']
                    creationTime = item['creationTime']
                    nickname = item['nickname']
                    productColor = item['productColor']
                    productSize = item['productSize']
                    userClientShow = item['userClientShow']
                    userLevelName = item['userLevelName']
                    sql_insert = ''
                    try:
                        sql_insert = "insert into jingdong_comment(anonymousFlag, content, creationTime, nickname, productColor, " \
                                     "productSize, userClientShow, userLevelName, jd_key) VALUES " \
                                     "('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"\
                                     % (anonymousFlag, content.strip(), creationTime, nickname, productColor, productSize,
                                        userClientShow, userLevelName, id)
                        self.cursor.execute(sql_insert)
                        self.connect.commit()
                        print('插入成功: ', sql_insert)
                        print('b-----%d' % b)
                        b += 1
                    except Exception as e:
                        print('error: ', sql_insert, e)

                print('comment_page: ', comment_page, 'comment_max_page: ', comment_max_page)
                if comment_page == comment_max_page:
                    comment_page = 0
                    break
                comment_page += 1

    def main(self):
        pool = multiprocessing.Process(target=self.parse, )
        pool.start()
        while self.page < 100:
            self.page += 1

        pool.join()


if __name__ == '__main__':
    JingDong().main()