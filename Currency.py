import time
from selenium import webdriver
from unidecode import unidecode
import requests
from bs4 import BeautifulSoup
import json
import jdatetime
import concurrent.futures

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
browser = webdriver.Chrome()


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
    browser.get(url[2])
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    prices = soup.find_all('strong')
    tether = unidecode(prices[5].text)
    tether = tether.split(',')
    tether = int(tether[0] + tether[1])
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


class Currency:
    def __init__(self):
        self.price = [0, 0, 0]
        self.tether = 0
        self.crypto_prices = None

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
    """login_url = 'https://wallex.ir/app/auth/login'
    with requests.Session() as s:
        pay_load = {
            'email': 'amirbehzadfar.h%40gmail.com',
            'password': '9*bzR%24C2fMAkLLq'
        }
        p = s.post(login_url, data=pay_load)
        #print(p.text)
        r = s.get('https://wallex.ir/markets/usdt-tmn')
        print(r.text)
    
    browser.get('https://wallex.ir/app/auth/login')
    email = browser.find_element_by_id("email")
    email.clear()
    email.send_keys("amirbehzadfar.h@gmail.com")

    password = browser.find_element_by_name("password")
    password.clear()
    password.send_keys("9*bzR$C2fMAkLLq")
    browser.find_element_by_class_name('signup-btn').click()
    browser.quit()"""
    print(get_tether_price())
