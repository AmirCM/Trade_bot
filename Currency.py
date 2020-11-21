import time
from selenium import webdriver
from unidecode import unidecode
import requests
from bs4 import BeautifulSoup
import json
import jdatetime

persian = {'BTC': 'بیت‌کوین (BTC)‏',
           'ETH': 'اتریوم (ETH)‏ ',
           'XMR': ' مونرو (XMR)‏ ',
           'DASH': ' دش (DASH)‏ ',
           'LTC': 'لایت کوین (LTC)‏ ',
           'USDT': ' تتر (USDT)‏ ',
           'ADA': 'کاردانو (ADA)‏ ',
           'TRX': ' ترون (TRX)‏ '}

post_text = ['📉 دلار', '📉 یورو', '📉 پوند انگلیس']
sell = '👈 نرخ فروش: '
buy = '👈🏼 خرید از مشتری: '


def get_page_data():
    tic = time.perf_counter()
    url = 'https://wallex.ir/'
    browser = webdriver.PhantomJS()
    browser.get(url)
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    prices = soup.find_all('strong')
    print('Tether elapse time {:.2f}'.format(time.perf_counter() - tic))
    return unidecode(prices[5].text)


def separator(p: str):
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
        self.url = ['https://www.tgju.org/', 'https://web-api.coinmarketcap.com/v1/cryptocurrency/'
                                             'listings/latest?aux=circulating_supply,max_supply,total_'
                                             'supply&convert=USD&cryptocurrency_type=all&limit=100&sort=market'
                                             '_cap&sort_dir=desc&start=1']
        self.price = [0, 0, 0]
        self.crypto = {'Bitcoin': 'BTC',
                       'Ethereum': 'ETH',
                       'Monero': 'XMR',
                       'Dash': 'DASH',
                       'Litecoin': 'LTC',
                       'Tether': 'USDT',
                       'Cardano': 'ADA',
                       'TRON': 'TRX'}

        self.c_keys = ['price_dollar_rl', 'price_eur', 'price_gbp']

    def to_rial(self, c_prices):
        tether = get_page_data()
        tether = tether.split(',')
        tether = int(tether[0] + tether[1])

        for k, v in c_prices.items():
            c_prices[k] = int(float(v) * tether)

        c_prices['USDT'] = tether
        return c_prices

    def update_db(self):
        r = requests.get(self.url[0])
        soup = BeautifulSoup(r.text, features='lxml')
        divs = soup.find_all('div', class_='home-fs-row')
        d_in_d = []
        for d in divs:
            d_in_d += d.find_all('table', class_='data-table market-table dark-head market-section-right')
        d_in_d = d_in_d[0]

        for i in range(3):
            price = d_in_d.find('tr', {"data-market-row": self.c_keys[i]}).find('td', {'class': 'nf'}).text.split(
                ',')
            self.price[i] = int(price[0]) * 100 + int(price[1]) // 10

        r = requests.get(self.url[1])
        data = json.loads(r.text)
        data = data['data']
        c_price = {}
        for d in data:
            if d['name'] in self.crypto:
                c_price[self.crypto[d['name']]] = str(d['quote']['USD']['price'])

        # c_price['USDT'] = str(1 + round(float(c_price['USDT']) - int(float(c_price['USDT'])), 5) * 10)
        return c_price

    def post_reporter(self):
        tic = time.perf_counter()

        c_prices = self.update_db()
        rials = self.to_rial(c_prices.copy())

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
            text += str(round(float(c_prices[k]), 3)) + '$' + '\n'
            text += sell + separator(str(v)) + '\n'
            text += buy + separator(str(int(v * 0.99))) + '\n\n'
        print('Reporting elapse time {:.2f}'.format(time.perf_counter() - tic))
        return text + '\n @keep_exchange \n'


if __name__ == '__main__':
    c = Currency()
    print(c.post_reporter())
