import requests
import execjs
import json


def analysis_js():
    node = execjs.get()

    method = 'GETDAYDATA'
    month = '201801'
    city = '杭州'

    ctx = node.compile(open('weather.js').read())
    params = ctx.eval('getEncryptedData("{month}", "{city}", "{method}")'.format(month=month, city=city, method=method))

    response = requests.post('https://www.aqistudy.cn/historydata/api/historyapi.php', data={'hd': params})

    decrypted_data = ctx.eval('decodeData("{response}")'.format(response=response.text))

    data = json.loads(decrypted_data)
    for item in data['result']['data']['items']:
        print(item)


if __name__ == '__main__':
    analysis_js()