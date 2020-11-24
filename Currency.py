import time
from selenium import webdriver
from unidecode import unidecode
import requests
from bs4 import BeautifulSoup
import json
import jdatetime
import concurrent.futures
import sched, time
import json

persian = {'BTC': 'بیت‌کوین (BTC)‏',
           'ETH': 'اتریوم (ETH)‏ ',
           'XMR': ' مونرو (XMR)‏ ',
           'DASH': ' دش (DASH)‏ ',
           'LTC': 'لایت کوین (LTC)‏ ',
           'USDT': ' تتر (USDT)‏ ',
           'ADA': 'کاردانو (ADA)‏ ',
           'TRX': ' ترون (TRX)‏ '}

crypto = {'Bitcoin': 'BTC',
          'Ethereum': 'ETH',
          'Monero': 'XMR',
          'Dash': 'DASH',
          'Litecoin': 'LTC',
          'Tether': 'USDT',
          'Cardano': 'ADA',
          'TRON': 'TRX'}

c_keys = ['price_dollar_rl', 'price_eur', 'price_gbp']
post_text = ['📉 دلار', '📉 یورو', '📉 پوند انگلیس']
sell = '👈 نرخ فروش: '
buy = '👈🏼 خرید از مشتری: '
url = ['https://www.tgju.org/', 'https://web-api.coinmarketcap.com/v1/cryptocurrency/'
                                'listings/latest?aux=circulating_supply,max_supply,total_'
                                'supply&convert=USD&cryptocurrency_type=all&limit=100&sort=market'
                                '_cap&sort_dir=desc&start=1', 'https://wallex.ir/']
template = """
⬇️ حداقل خرید: 0.001 بیت‌کوین، معادل:500,200 تومان
⬆️ حداکثر خرید: 1 بیت‌کوین، معادل:500,212,000 تومان

⏰ مهلت تکمیل سفارش: 18:18:13

✅ لطفا یکی از گزینه های زیر را انتخاب نمایید:"""


def get_cash_price():
    results = [0, 0, 0]
    r = requests.get(url[0])
    soup = BeautifulSoup(r.text, features='lxml')
    divs = soup.find_all('div', class_='home-fs-row')
    d_in_d = []
    for d in divs:
        d_in_d += d.find_all('table', class_='data-table market-table dark-head market-section-right')
    d_in_d = d_in_d[0]
    for i in range(3):
        price = d_in_d.find('tr', {"data-market-row": c_keys[i]}).find('td', {'class': 'nf'}).text.split(
            ',')
        results[i] = int(price[0]) * 100 + int(price[1]) // 10
    return results


def get_crypto_price():
    r = requests.get(url[1])
    data = json.loads(r.text)
    data = data['data']
    c_price = {}
    for d in data:
        if d['name'] in crypto:
            c_price[crypto[d['name']]] = str(d['quote']['USD']['price'])
    return c_price


def get_tether_price():
    data = {
        "srcCurrency": "usdt", "dstCurrency": "rls"
    }
    r = requests.post('https://api.nobitex.ir/market/stats', data=data)
    tether = int(float(r.json()['stats']['usdt-rls']['latest']) // 10)
    return tether


def separator(p: str):
    i = 3 - len(p) % 3
    rs = ''
    for j, ch in enumerate(p):
        if (j + i) % 3 == 0 and j != 0:
            rs += ',' + ch
        else:
            rs += ch
    return rs


def separator_int(p: int):
    p = str(p)
    i = 3 - len(p) % 3
    rs = ''
    for j, ch in enumerate(p):
        if (j + i) % 3 == 0 and j != 0:
            rs += ',' + ch
        else:
            rs += ch
    return rs


class Currency:
    def __init__(self):
        self.price = [0, 0, 0]
        self.tether = 0
        self.crypto_prices = None
        self.min_prices = None

    def to_rial(self, c_prices):
        c_prices = c_prices.copy()
        for k, v in c_prices.items():
            c_prices[k] = int(float(v) * self.tether)

        c_prices['USDT'] = self.tether
        return c_prices

    def get_prices(self):
        tic = time.perf_counter()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            ex1 = executor.submit(get_tether_price)
            ex2 = executor.submit(get_cash_price)
            ex3 = executor.submit(get_crypto_price)

        self.tether = ex1.result()
        self.price = ex2.result()
        self.crypto_prices = ex3.result()
        print(f'elapse time {time.perf_counter() - tic:.2f}')

    def post_reporter(self):
        rials = self.to_rial(self.crypto_prices)

        rials = {k: v for k, v in sorted(rials.items(), key=lambda item: item[1], reverse=True)}

        x = jdatetime.datetime.now()
        text = '📅 تاریخ: ' + x.strftime('%x') + '\n' + '⏰ ساعت: ' + x.strftime('%X') + '\n'
        for i, p in enumerate(post_text):
            text += p + '\n' + sell + separator(str(self.price[i])) + '\n' + buy + \
                    separator(str(int(self.price[i] * 0.99))) + '\n\n'

        text += '📌نرخ بروز ارزهای دیجیتال: '
        text += '\nــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ\n'

        emoji = '📉'
        for k, v in rials.items():
            text += emoji + '\t' + persian[k] + ':'
            text += str(round(float(self.crypto_prices[k]), 3)) + '$' + '\n'
            text += sell + separator(str(v)) + '\n'
            text += buy + separator(str(int(v * 0.99))) + '\n\n'
        return text + '\n @keep_exchange \n'

    def minimum_calc(self):
        self.min_prices = self.to_rial(self.crypto_prices)
        criterion = self.min_prices['USDT'] * 10
        for k, v in self.min_prices.items():
            _min = int((criterion / v) * 10000)
            _min /= 10000.0
            if _min > 1:
                _min = int(_min)
            self.min_prices[k] = [v, _min, int(_min * v)]

    def minimum_reporter(self, c_type, type):
        txt = '👈 ارز انتخابی شما: '
        txt += persian[c_type]
        txt += '\n'
        if type is True:
            txt += f'💵 قیمت واحد: {separator_int(int(self.min_prices[c_type][0] * 0.99))} تومان '
            txt += '\n'
            txt += f'⬇️ حداقل ارزش معامله: {self.min_prices[c_type][1]} {c_type}، معادل: {separator_int(self.min_prices[c_type][2] * 0.99)} تومان'
            txt += '\n'
            txt += 'مقدار مورد نظر خود را برای خرید را به عدد وارد نمایید: '
        else:
            txt += f'💵 قیمت واحد: {separator_int(int(self.min_prices[c_type][0]))} تومان '
            txt += '\n'
            txt += f'⬇️ حداقل ارزش معامله: {self.min_prices[c_type][1]} {c_type}، معادل: {separator_int(self.min_prices[c_type][2])} تومان'
            txt += '\n'
            txt += 'مقدار مورد نظر خود را برای فروش را به عدد وارد نمایید: '
        txt += '\n'
        return txt


"""i = 0
def do_something(sc):
    global i
    print(f"Doing stuff... {i}")
    # do your stuff
    i += 1
    s.enter(5, 1, do_something, (sc,))"""

if __name__ == '__main__':
    """
    s = sched.scheduler(time.time, time.sleep)
    s.enter(5, 1, do_something, (s,))
    s.run()

    """
    c = Currency()
    c.get_prices()
    c.minimum_calc()
    print(c.min_prices)
