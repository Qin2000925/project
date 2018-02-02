import requests
import execjs
import json


def analysis_js():
    node = execjs.get()

    method = 'GETDAYDATA'
    month = '201801'
    city = '杭州'

    file = 'weather.js'
    ctx = node.compile(open(file).read())

    js = 'getEncryptedData("{month}", "{city}", "{method}")'.format(month=month, city=city, method=method)
    params = ctx.eval(js)

    api = 'https://www.aqistudy.cn/historydata/api/historyapi.php'
    response = requests.post(api, data={'hd': params})

    js = 'decodeData("{0}")'.format(response.text)
    decrypted_data = ctx.eval(js)
    data = json.loads(decrypted_data)
    for item in data['result']['data']['items']:
        print(item)


if __name__ == '__main__':
    analysis_js()