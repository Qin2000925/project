import requests
import pymysql
import time


class XieChen(object):
    def __init__(self, checkIn, checkOut):
        self.url = 'http://hotels.ctrip.com/Domestic/Tool/AjaxHotelList.aspx'
        self.session = requests.session()

        self.headers = {
            'Host': 'hotels.ctrip.com',
            'Origin': 'http://hotels.ctrip.com',
            'Referer': 'http://hotels.ctrip.com/hotel/hangzhou17',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
        }
        self.page = 1

        self.checkIn = checkIn
        self.checkOut = checkOut

        self.connect = pymysql.connect(host='127.0.0.1', db='djangomysql', password='qinjiahu521', user='root', charset='utf8')
        self.cursor = self.connect.cursor()

        self.text_url = 'http://hotels.ctrip.com/{full}&checkIn={checkIn}&checkOut={checkOut}#{ctm_ref}'

    def parse(self):
        while self.page < 300:
            data = {
                '__VIEWSTATEGENERATOR': 'DB1FBB6D',
                'cityName': '%E6%9D%AD%E5%B7%9E',
                'StartTime': self.checkIn,
                'DepTime': self.checkOut,
                'txtkeyword': '',
                'Resource': '',
                'Room': '',
                'Paymentterm': '',
                'BRev': '',
                'Minstate': '',
                'PromoteType': '',
                'PromoteDate': '',
                'operationtype': 'NEWHOTELORDER',
                'PromoteStartDate': '',
                'PromoteEndDate': '',
                'OrderID': '',
                'RoomNum': '',
                'IsOnlyAirHotel': 'F',
                'cityId': '17',
                'cityPY': 'hangzhou',
                'cityCode': '0571',
                'cityLat': '30.2799952044',
                'cityLng': '120.1616127798',
                'positionArea': '',
                'positionId': '',
                'hotelposition': '',
                'keyword': '',
                'hotelId': '',
                'htlPageView': '0',
                'hotelType': 'F',
                'hasPKGHotel': 'F',
                'requestTravelMoney': 'F',
                'isusergiftcard': 'F',
                'useFG': 'F',
                'HotelEquipment': '',
                'priceRange': '-2',
                'hotelBrandId': '',
                'promotion': 'F',
                'prepay': 'F',
                'IsCanReserve': 'F',
                'OrderBy': '99',
                'OrderType': '',
                'k1': '',
                'k2': '',
                'CorpPayType': '',
                'viewType': '',
                'checkIn': '2018-01-17',
                'checkOut': '2018-01-25',
                'DealSale': '',
                'ulogin': '',
                'hidTestLat': '0%7C0',
                'AllHotelIds': '435383%2C346316%2C429778%2C5918673%2C7828854%2C346311%2C435427%2C1435183%2C346313%2C429719%2C5903375%2C375490%2C10558548%2C435361%2C532788%2C3997628%2C5240879%2C396983%2C1674636%2C346307%2C6232941%2C1207757%2C435419%2C8602465%2C375371',
                'psid': '',
                'HideIsNoneLogin': 'T',
                'isfromlist': 'T',
                'ubt_price_key': 'htl_search_result_promotion',
                'showwindow': '',
                'defaultcoupon': '',
                'isHuaZhu': 'False',
                'hotelPriceLow': '',
                'htlFrom': 'hotellist',
                'unBookHotelTraceCode': '',
                'showTipFlg': '',
                'hotelIds': '435383_1_1,346316_2_1,429778_3_1,5918673_4_1,7828854_5_1,346311_6_1,435427_7_1,1435183_8_1,346313_9_1,429719_10_1,5903375_11_1,375490_12_1,10558548_13_1,435361_14_1,532788_15_1,3997628_16_1,5240879_17_1,396983_18_1,1674636_19_1,346307_20_1,6232941_21_1,1207757_22_1,435419_23_1,8602465_24_1,375371_25_1',
                'markType': '0',
                'zone': '',
                'location': '',
                'type': '',
                'brand': '',
                'group': '',
                'feature': '',
                'equip': '',
                'star': '',
                'sl': '',
                's': '',
                'l': '',
                'price': '',
                'a': '0',
                'keywordLat': '',
                'keywordLon': '',
                'contrast': '0',
                'page': self.page,
                'contyped': '0',
                'productcode': ''
            }
            response = self.session.post(self.url, headers=self.headers, data=data).json()['hotelPositionJSON']
            for item in response:
                t = int(time.time())
                time_local = time.localtime(t)
                dt = time.strftime('%Y-%m-%d', time_local)
                url = item['url'].split('#')
                url = self.text_url.format(full=url[0], checkIn=self.checkIn, checkOut=self.checkOut, ctm_ref=url[1])
                insert_sql = "insert into xiecheng(name, address, star_desc, dp_score, dp_count, url, get_id, lat, lon, score, " \
                             "short_name, add_time) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"\
                             % (item['name'], item['address'], item['stardesc'], item['dpscore'], item['dpcount'], url,
                                item['id'], item['lat'], item['lon'], item['score'], item['shortName'], dt)
                self.cursor.execute(insert_sql)
                self.connect.commit()
                print('插入成功: ', insert_sql)
            time.sleep(2)
            self.page += 1
        self.connect.close()


if __name__ == '__main__':
    XieChen('2018-01-23', '2018-01-28').parse()

