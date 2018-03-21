import requests
import json
from hbsdk import ApiClient, ApiError
import MySQLdb

cny_to_usdt = 7.73
coins = ['btc','ltc','eth','etc','eos','qtum','hsr','xrp']

# 打开数据库连接
db = MySQLdb.connect("127.0.0.1","root","root","hack" )
# 使用cursor()方法获取操作游标
cursor = db.cursor()
cursor.execute('set TIME_ZONE="+08:00"')

def huobi_usdt_price(coin_type):
    API_KEY = 'd0ece565-9908ceb4-3a1fae05-7a813'
    API_SECRET = 'ebd261e6-222d8e94-f058cd95-1524c'
    client = ApiClient(API_KEY, API_SECRET)
    trade = client.get('/market/trade', symbol=coin_type+'usdt')
    return trade['tick']['data'][0]['price']


def zb_qc_price(coin_type):
    coin_type = coin_type + '_qc'
    response = requests.get("http://api.zb.com/data/v1/ticker?market=" + coin_type)
    coin_price =json.loads(response.text)
    return float(coin_price['ticker']['last'])


def okex_price(coin):
    coin = coin + "_usdt"
    response = requests.get("https://www.okex.com/api/v1/ticker.do?symbol=" + coin)
    coin_price = json.loads(response.text)
    return float(coin_price['ticker']['last'])

if __name__ == '__main__':
    while(True):
        print('币种 zb_qc_price  zb_us_price   huobi_usdt   okex         zb/huobi    huobi/okex')
        for coin in coins:
            try:
                zb_price = zb_qc_price(coin)
                zb_usdt_price = round(zb_price / cny_to_usdt, 2)
                huobi_price = huobi_usdt_price(coin)
                okex = okex_price(coin)
                zb_hb_diff_price = round((zb_usdt_price - huobi_price) / huobi_price * 100, 4)
                hb_okex_diff_price = round((huobi_price-okex)/okex, 4)
                print('{0:<4} {1:<12} {2:<12} {3:<12} {4:<12} {5:<12} {6}'.format(coin, zb_price, zb_usdt_price, huobi_price, okex, zb_hb_diff_price, hb_okex_diff_price))
                # print('{0:<4} {1:<12} {2:<12} {3:<12} {4}'.format(coin, zb_price, zb_usdt_price, huobi_price, zb_hb_diff_price))
                if zb_hb_diff_price < -5 or zb_hb_diff_price > 5:
                    # requests.get('http://hippo-studio.com/api/cookie?website=diff_price-{0}--zb-{1}--huobi-{2}'.format(coin,zb_price,huobi_price))
                    sql = "insert into arbitrage_log(coin, zb, zb_usdt, huobi, diff_price) values('{0}','{1}','{2}','{3}','{4}')".format(coin,zb_price,zb_usdt_price,huobi_price,zb_hb_diff_price)
                    cursor.execute(sql)
                    db.commit()
            except Exception as e:
                print(e)
                db.rollback()
                pass