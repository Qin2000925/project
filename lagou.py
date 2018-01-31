import requests
import json
import pymysql
import time
import random
import lxml.html


class LaGou(object):
    def __init__(self):
        self.url = 'https://www.lagou.com/jobs/positionAjax.json?city=%s&needAddtionalResult=false&isSchoolJob=0'
        self.headers = {
            'Host': 'www.lagou.com',
            'Origin': 'https://www.lagou.com',
            'Referer': 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
            'X-Anit-Forge-Code': '0',
            'X-Anit-Forge-Token': 'None',
            'X-Requested-With': 'XMLHttpRequest'}

        self.session = requests.session()

        self.connect = pymysql.connect(host='127.0.0.1', user='root', password='qinjiahu521', db='djangomysql', charset='utf8')
        self.cursor = self.connect.cursor()

    def get_text(self):
        headers = {
            'Host': 'www.lagou.com',
            'Referer': 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
        }
        response = self.session.get('https://www.lagou.com/', headers=headers)
        get_html = lxml.html.fromstring(response.text)
        classification = get_html.xpath('//*[@class="menu_sub dn"]/dl/dd/a/text()')
        self.parse(list(set(classification)))

    def parse(self, class_list):
        for i in class_list:
            pn = 1
            while pn < 30:
                time.sleep(random.randint(1, 2))
                data = {
                    'first': 'true',
                    'pn': pn,
                    'kd': i
                }
                response = self.session.post(self.url  % '杭州', headers=self.headers, data=data)
                json_item = json.loads(response.text)
                print(json_item)

                json_content = json_item['content']['positionResult']['result']

                for item in json_content:
                    companyFullName = item['companyFullName']
                    positionName = item['positionName']
                    salary = item['salary']
                    secondType = item['secondType']
                    positionAdvantage = item['positionAdvantage']
                    companySize = item['companySize']
                    positionId = item['positionId']
                    city = item['city']
                    companyShortName = item['companyShortName']
                    createTime = item['createTime']
                    firstType = item['firstType']
                    financeStage = item['financeStage']
                    companyLabelList = item['companyLabelList']
                    industryField = item['industryField']
                    workYear = item['workYear']
                    education = item['education']
                    jobNature = item['jobNature']
                    job_url = 'https://www.lagou.com/jobs/{}.html'.format(positionId)

                    companyLabel = ', '.join(companyLabelList)
                    t = int(time.time())
                    time_local = time.localtime(t)
                    dt = time.strftime("%Y-%m-%d", time_local)

                    sql_insert = "insert into lagou(companyFullName, positionName, salary, secondType, positionAdvantage, companySize, " \
                                 "positionId, city, companyShortName, createTime, firstType, financeStage, companyLabelList, " \
                                 "industryField, workYear, education, jobNature, job_url, add_time) VALUES ('%s', '%s', '%s', '%s', " \
                                 "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
                                 % (companyFullName, positionName, salary, secondType, positionAdvantage, companySize, positionId,
                                    city, companyShortName, createTime, firstType, financeStage, companyLabel, industryField,
                                    workYear, education, jobNature, job_url, dt)
                    self.cursor.execute(sql_insert)
                    self.connect.commit()
                    print('插入成功: ', sql_insert)
                pn += 1


if __name__ == '__main__':
    LaGou().get_text()