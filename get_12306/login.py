import requests
from PIL import Image
from json import loads
from region import cons
import time
import urllib.parse
import re


session = requests.session()

list_dict = {
    '软卧': 23,
    '硬卧': 28,
    '硬座': 29,
    '无座': 26,
    '车次': 3,
    '出发时间': 8,
    '到达时间': 9,
    '历时': 10,
    '商务座': 32,
    '一等座': 31,
    '二等座': 30
}

station_dict = {}
for i in cons.split('@'):
    if i:
        tmp_list = i.split('|')
        station_dict[tmp_list[1]] = tmp_list[2]


class LoginTic(object):
    def __init__(self):
        self.headers = {
            'Host': 'kyfw.12306.cn',
            'Referer': 'https://kyfw.12306.cn/otn/login/init',
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
        }

    def getImg(self):
        url = "https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&0.7522476342786162"
        response = session.get(url=url, headers=self.headers, verify=False)

        with open('login_img.jpg', 'wb') as f:
            f.write(response.content)
        im = Image.open('login_img.jpg')
        im.show()
        captcha_solution = input('请输入验证码位置，以","分割[例如2,5]:')
        return captcha_solution

    def checkYanZheng(self, solution):
        soList = solution.split(',')
        yanSol = ['43,48', '115,48', '189,48', '259,48', '45,121', '114,121', '186,121', '255,121']
        yanList = []
        for item in soList:
            yanList.append(yanSol[int(item)])
        yanStr = ','.join(yanList)
        checkUrl = "https://kyfw.12306.cn/passport/captcha/captcha-check"
        data = {
            'answer': yanStr,
            'login_site': 'E',
            'rand': 'sjrand'
        }
        while True:
            try:
                cont = session.post(url=checkUrl, data=data, headers=self.headers, verify=False)
                result = loads(cont.content)
                print('验证码验证: ', result)
                code = result.get('result_message', 'bank')

                if code == 'bank':
                    print('验证码验证网络出现问题，延时2秒')
                    time.sleep(2)
                    continue
                if code == u'验证码校验成功':
                    print('验证通过!', code)
                    return True
                else:
                    print('验证失败，请重新验证!', code)
                    return False
            except Exception as e:
                print('验证码验证出现异常，延时2秒', e)
                time.sleep(2)

    def loginTo(self):
        time.sleep(1)
        login_headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '52',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'kyfw.12306.cn',
            'Referer': 'https://kyfw.12306.cn/otn/login/init',
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
            'X-Requested-With': 'XMLHttpRequest'
        }
        loginUrl = "https://kyfw.12306.cn/passport/web/login"
        data = {
            'username': '',
            'password': '',
            'appid': 'otn'
        }
        time.sleep(2)
        while True:
            try:
                result = session.post(url=loginUrl, data=data, headers=login_headers, verify=False)
                result.encoding = 'utf-8'
                dic = loads(result.content)
                mes = dic['result_message']
                if mes == u'登录成功':
                    print('恭喜你，登录成功，可以购票!', result)
                    return True
                else:
                    print('对不起，登录失败，请检查登录信息!', result)
                    return False
            except Exception as e:
               print('用户验证网络出现异常，延时2秒', e)
               time.sleep(2)

    def login_info(self):
        login_headers = {
            'Host': 'kyfw.12306.cn',
            'Origin': 'https://kyfw.12306.cn',
            'Referer': 'https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        auth_data = {'appid': 'otn'}
        auth_url = 'https://kyfw.12306.cn/passport/web/auth/uamtk'
        while True:
            try:
                auth_response = session.post(auth_url, headers=login_headers, verify=False, data=auth_data)
                result = loads(auth_response.text).get('result_message', 'bank')
                tk = loads(auth_response.text).get('newapptk', 'bank')

                if result == 'bank':
                    print('auth验证网络出现问题，延时2秒: ', result)
                    time.sleep(2)
                    continue
                if result == '验证通过':
                    print('auth验证成功: ', result)
                    break
            except Exception as e:
                print('auth验证网络出现异常，延时2秒', e)
                time.sleep(2)

        uam_auth_client_url = 'https://kyfw.12306.cn/otn/uamauthclient'
        uam_auth_client_data = {'tk': tk}
        while True:
            try:
                uam_auth_client_response = session.post(uam_auth_client_url, headers=login_headers,
                                                        data=uam_auth_client_data, verify=False)
                print(uam_auth_client_response.text)
                result = loads(uam_auth_client_response.text).get('result_message', 'bank')
                if result == 'bank':
                    print('uam_auth_client验证网络出现问题，延时2秒: ', result)
                    time.sleep(2)
                    continue
                if result == '验证通过':
                    print('uam_auth_client验证: ', result)
                    # break
                    return True
            except Exception as e:
                print('uam_auth_client验证网络出现异常，延时2秒', e)
                time.sleep(2)

        # headers = {
        #     'Host': 'kyfw.12306.cn',
        #     'Referer': 'https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin',
        #     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
        # }
        # session.get('https://kyfw.12306.cn/otn/index/initMy12306', headers=headers, verify=False)
        #
        # user_login = 'https://kyfw.12306.cn/otn/login/userLogin'
        # user_headers = {
        #     'Host': 'kyfw.12306.cn',
        #     'Referer': 'https://kyfw.12306.cn/otn/login/init',
        #     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
        # }
        # while True:
        #     try:
        #         user_response = session.post(user_login, data={'_json_att': ''}, verify=False, headers=user_headers)
        #         print('user_response: ', user_response.text)
        #         result1 = loads(user_response.text).get('status', 'bank')
        #         result2 = loads(user_response.text).get('data', 'bank').get('flag')
        #         if result1 == 'bank':
        #             print('checkUser验证网络出现问题，延时2秒')
        #             time.sleep(2)
        #             continue
        #         if result1 == True and result2 == True:
        #             print('checkUser验证:', result1, result2)
        #             return True
        #         else:
        #             print('用户检测不在状态，退出')
        #             return False
        #     except Exception as e:
        #         print('checkUser验证出现异常，延时2秒', e)
        #         time.sleep(2)


class InsertTicket(object):
    def __init__(self, seat, date, from_station, to_station, train):
        self.headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        self.seat = seat
        self.date = date
        self.from_station = from_station
        self.to_station = to_station
        self.train = train

    def get_ticket(self):
        print('开始查余票......')
        from_station = station_dict[self.from_station]
        to_station = station_dict[self.to_station]
        print('from_station: ', from_station)
        print('to_station: ', to_station)

        url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=%s&leftTicketDTO.from_station=%s&' \
              'leftTicketDTO.to_station=%s&purpose_codes=ADULT' % (self.date, from_station, to_station)
        fail = 0
        while True:
            try:
                if fail >= 10:
                    print('查余票出现异常10次，取消')
                    return False
                response = session.get(url, headers=self.headers, verify=False)
                json_item = loads(response.text)
                if fail < 10:
                    break
            except Exception as e:
                print(e)
                fail += 1
                print('查余票出现异常 %d 次,重新发送' % fail)
            print('延时两秒......')
            time.sleep(2)
        results = []
        for item in json_item['data']['result']:
            items = item.split('|')
            if str(self.train) in items:
                results.append(items)
        return results

    def ticket(self):
        nn = 1
        lists = []
        while True:
            results = self.get_ticket()
            print('results: ', results)
            for lists in results:
                n = list_dict[self.seat]
                if lists[n] == '无' or lists[n] == '':
                    continue
                elif lists[n] == '有':
                    info = '%s--有票  ' % self.seat, '车次:%s ' % lists[3], '行程：{} -> {}  '.format(self.from_station, self.to_station), \
                          '出发时间:%s %s  ' % (self.date, lists[8]), '到达时间:%s %s' % (self.date, lists[9]), '历时: %s' % lists[10]
                    return lists, True, info
                elif str(lists[n]).isdigit():
                    info = '%s有票' % self.seat, '车次:%s ' % lists[3], '行程：{} -> {}  '.format(self.from_station, self.to_station), \
                           '出发时间:%s %s' % (self.date, lists[8]), '到达时间:%s %s' % (self.date, lists[9]), '历时: %s' % lists[10]
                    return lists, True, info
            print('查票次数: %d次, %s无票' % (nn, self.seat))
            if nn >= 10:
                return lists, False
            nn += 1
            print('延时两秒......')
            time.sleep(2)

    def post_data(self, secretStr, info):
        headers = {
            'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

        checkUser_url = 'https://kyfw.12306.cn/otn/login/checkUser'
        checkUser_response = session.post(checkUser_url, data={'_json_att': ''}, headers=headers, verify=False)
        print('checkUser_response: ', checkUser_response.text)

        submit_order_request_data = {
            'secretStr': urllib.parse.unquote(secretStr[0]),
            'train_date': self.date,
            'back_train_date': '2018-01-20',
            'tour_flag': 'dc',
            'purpose_codes': 'ADULT',
            'query_from_station_name': '杭州',
            'query_to_station_name': '阜阳',
            'undefined': ''
        }
        time.sleep(2)
        #  {"validateMessagesShowId":"_validatorMessage","status":true,"httpstatus":200,"data":"Y","messages":[],"validateMessages":{}}
        submit_order_request_url = 'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'
        while True:
            try:
                submit_order_response = session.post(submit_order_request_url, data=submit_order_request_data,
                                                     verify=False, headers=headers)
                result1 = loads(submit_order_response.text).get('status', 'bank')
                result2 = loads(submit_order_response.text).get('messages', 'bank')

                if result1 == 'bank':
                    print('submitOrderRequest请求网络出现问题，延时2秒: ', submit_order_response.text)
                    time.sleep(2)
                    continue
                if result1 == True and result2 == []:
                    print('submitOrderRequest请求通过: ', submit_order_response.text)
                    break
                else:
                    print('submitOrderRequest请求出现问题,退出', submit_order_response.text)
                    return False
            except Exception as e:
                print('submitOrderRequest请求出现异常，延时2秒', e)
                time.sleep(2)

        print('\n' + '-' * 100 + '\n')
        time.sleep(2)

        get_passenger_init_headers = {
            'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
        }
        get_passenger_init_data = {
            '_json_att': ''
        }
        get_passenger_init_url = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
        while True:
            try:
                get_passenger_init_response = session.post(url=get_passenger_init_url, data=get_passenger_init_data,
                                                           headers=get_passenger_init_headers, verify=False)

                REPEAT_SUBMIT_TOKEN = re.findall("var globalRepeatSubmitToken = '(.*?)';", get_passenger_init_response.text, re.S)
                KEY_CHECK_ISCHANGE = re.findall("key_check_isChange':'(.*?)'",get_passenger_init_response.text , re.S)
                print('REPEAT_SUBMIT_TOKEN: ', REPEAT_SUBMIT_TOKEN)
                print('KEY_CHECK_ISCHANGE: ', KEY_CHECK_ISCHANGE)
                if not KEY_CHECK_ISCHANGE:
                    print('initDc网络出现问题，退出: ', KEY_CHECK_ISCHANGE)
                    return False
                break
            except Exception as e:
                print('initDc出现异常，延时2秒', e)
                time.sleep(2)

                print('\n' + '-' * 100 + '\n')
        time.sleep(1)

        get_passenger_data = {
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': REPEAT_SUBMIT_TOKEN[0]
        }
        # {"validateMessagesShowId":"_validatorMessage","status":true,
        get_passenger_url = 'https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs'

        get_passenger_headers = {
            'Content-Length': '63',
            'Referer': 'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Host': 'kyfw.12306.cn',
        }

        while True:
            try:
                get_passenger_response = session.post(get_passenger_url, data=get_passenger_data,
                                                      verify=False, headers=get_passenger_headers)

                result1 = loads(get_passenger_response.text).get('status', 'bank')

                if result1 == 'bank':
                    print('getPassengerDTOs请求网络出现问题，延时2秒: ', get_passenger_response.text)
                    time.sleep(2)
                    continue
                if result1:
                    print('getPassengerDTOs请求通过: ', get_passenger_response.text)
                    break
                else:
                    print('getPassengerDTOs不在状态，退出: ', get_passenger_response.text)
                    return False
            except Exception as e:
                print('getPassengerDTOs请求出现异常，延时2秒', e)
                time.sleep(2)

        print('\n' + '-' * 100 + '\n')
        time.sleep(2)

        get_passenger_headers['Content-Length'] = '323'
        check_order_info_data = {
            'cancel_flag': '2',
            'bed_level_order_num': '000000000000000000000000000000',
            'passengerTicketStr': '1,0,1,晏军,1,342130197807095625,18368142790,N',
            'oldPassengerStr': '晏军,1,342130197807095625,1_',
            'tour_flag': 'dc',
            'randCode': '',
            'whatsSelect': '1',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': REPEAT_SUBMIT_TOKEN[0]
        }
        # {"validateMessagesShowId":"_validatorMessage","status":true,"httpstatus":200,"data":
        check_order_info_url = 'https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo'
        while True:
            try:
                check_order_info_response = session.post(url=check_order_info_url, headers=get_passenger_headers, verify=False,
                                                         data=check_order_info_data)

                result1 = loads(check_order_info_response.text).get('status', 'bank')

                if result1 == 'bank':
                    print('checkOrderInfo_data请求网络出现问题，延时2秒: ', check_order_info_response.text)
                    time.sleep(2)
                    continue
                if result1:
                    print('checkOrderInfo_data请求通过: ', check_order_info_response.text)
                    break
                else:
                    print('延时2s，重新请求上一步', check_order_info_response.text)

                    while True:
                        try:
                            headers['Referer'] = 'https://kyfw.12306.cn/otn/leftTicket/init'
                            response = session.post(submit_order_request_url, data=submit_order_request_data, verify=False,
                                                    headers=headers)
                            result1 = loads(response.text).get('status', 'bank')
                            result2 = loads(response.text).get('messages', 'bank')

                            if result1 == 'bank':
                                print('submit_order_request_url请求网络出现问题，延时2秒: ', response.text)
                                time.sleep(2)
                                continue
                            if result1 == True and result2 == []:
                                print('submit_order_request_url请求通过: ', response.text)
                                break
                            else:
                                print('submit_order_request_url请求出现问题,退出', response.text)
                                return False
                        except Exception as e:
                            print('submit_order_request_url请求出现异常，延时2秒', e)
                            time.sleep(2)
                    get_response= ''
                    while True:
                        try:
                            get_response = session.post(get_passenger_url, verify=False, data=get_passenger_data,
                                                        headers=get_passenger_headers)
                            result1 = loads(get_response.text).get('status', 'bank')

                            if result1 == 'bank':
                                print('get_passenger_url请求网络出现问题，延时2秒: ', get_response.text)
                                time.sleep(2)
                                continue
                            if result1:
                                print('get_passenger_url请求通过: ', get_response.text)
                                break
                            else:
                                print('get_passenger_url不在状态，退出: ', get_response.text)
                                return False
                        except Exception as e:
                            print(get_response.text)
                            print('get_passenger_url请求出现异常，延时2秒', e)
                            time.sleep(2)
                    time.sleep(2)
            except Exception as e:
                print('checkOrderInfo_data请求出现异常，延时2秒', e)
                time.sleep(2)

        print('\n' + '-' * 100 + '\n')

        get_queue_count_data = {
            'train_date': 'Sat Jan 20 2018 00:00:00 GMT+0800 (CST)',
            'train_no': secretStr[2],
            'stationTrainCode': secretStr[3],
            'seatType': '1',
            'fromStationTelecode': secretStr[6],
            'toStationTelecode': secretStr[7],
            'leftTicket': secretStr[12],
            'purpose_codes': '00',
            'train_location': secretStr[15],
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': REPEAT_SUBMIT_TOKEN[0]
        }
        # {"validateMessagesShowId":"_validatorMessage","status":true,"httpstatu
        # s":200,"data":{"count":"0","ticket":"0,109","op_2":"false","countT":"0","op_1":"false"},"messages":[],"validateMessages":{}}

        get_passenger_headers['Content-Length'] = '388'
        get_queue_count_url = 'https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount'
        queue_response = session.post(url=get_queue_count_url, headers=get_passenger_headers, verify=False, data=get_queue_count_data)
        print(queue_response.text)

        print('\n' + '-' * 100 + '\n')
        time.sleep(1.5)

        confirmSingleForQueue_data = {
            'passengerTicketStr': '1,0,1,晏军,1,342130197807095625,18368142790,N',
            'oldPassengerStr': '晏军,1,342130197807095625,1_',
            'randCode': '',
            'purpose_codes': '00',
            'key_check_isChange': KEY_CHECK_ISCHANGE[0],
            'leftTicketStr': secretStr[12],
            'train_location': secretStr[15],
            'choose_seats': '',
            'seatDetailType': '000',
            'whatsSelect': '1',
            'roomType': '00',
            'dwAll': 'N',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': REPEAT_SUBMIT_TOKEN[0]
        }
        # {"validateMessagesShowId":"_validatorMessage","status":true,"httpstatus":200,"data":{"submitStatus":true},"messages":[],"validateMessages":{}}
        confirmSingleForQueue_url = 'https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue'
        confirm_response = session.post(confirmSingleForQueue_url, data=confirmSingleForQueue_data, verify=False, headers=headers)
        print(confirm_response.text)

        print('恭喜你12306自动抢票成功--->  车票信息: ', info)


def main():
    insert_ticket = InsertTicket('无座', '2018-01-18', '杭州', '阜阳', 'K1050')
    lists, boolean, info = insert_ticket.ticket()

    if boolean:
        print('开始登录...')
        login = LoginTic()
        captcha_solution = login.getImg()
        get_check = login.checkYanZheng(captcha_solution)
        if get_check:
            if login.loginTo():
                if login.login_info():
                    insert_ticket.post_data(lists, info)
    return False


if __name__ == '__main__':
    # main()
    a = []
    print(''.join(a).strip())