import rules
import datetime
from telegram import *

# Stages
FIRST, SECOND, THIRD, FORTH, FIFTH, SIXTH = range(6)
# Callback data
ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN = range(7)

currency_name = {'Bitcoin': 'BTC',
                 'Ethereum': 'ETH',
                 'Monero': 'XMR',
                 'Dash': 'DASH',
                 'Litecoin': 'LTC',
                 'Tether': 'USDT',
                 'Cardano': 'ADA',
                 'TRON': 'TRX'}
persian = {'BTC': 'بیت‌کوین (BTC)‏',
           'ETH': 'اتریوم (ETH)‏ ',
           'XMR': ' مونرو (XMR)‏ ',
           'DASH': ' دش (DASH)‏ ',
           'LTC': 'لایت کوین (LTC)‏ ',
           'USDT': ' تتر (USDT)‏ ',
           'ADA': 'کاردانو (ADA)‏ ',
           'TRX': ' ترون (TRX)‏ '}

start_text = 'برای شروع تلفن خود را وارد کنید'
wellcome_text = """با سلام
    به دنیای دیجیتال خوش آمدید
    با کیپ مانی دنیای دیجیتال را تجربه کنید

برخی از امکانات این ربات 👇🏻👇🏻👇🏻
1⃣ خرید و فروش ارزهای دیجیتال
2⃣ احراز هویت آسان، منظم و سریع
    کاربر گرامی ,
🍀 حساب کاربری شما فعال است.
لطفاً عملیات مورد نظر خود را از منوی زیر انتخاب نمایید:"""

main_keyboard = [
    [
        InlineKeyboardButton("💵 معامله با ما", callback_data='deal'),
        InlineKeyboardButton("💳 کیف پول", callback_data='wallet'),
        InlineKeyboardButton("📈 بازارها", callback_data='market')
    ],
    [
        InlineKeyboardButton("💸 معرفی به دوستان", callback_data='recommend'),
        InlineKeyboardButton("👤 حساب کاربری", callback_data='account'),
        InlineKeyboardButton("⚖️ قوانین", callback_data='rules')
    ],
    [
        InlineKeyboardButton("💬 پشتیبانی", callback_data='service')
    ]
]
main_text = 'منوی اصلی '
deal_keyboard = [
    [
        InlineKeyboardButton("💵معاملات ارز حواله", callback_data='cash'),
        InlineKeyboardButton("💎معاملات ارز دیجیتال", callback_data='crypto'),
    ],
    [
        InlineKeyboardButton("↩️بازگشت", callback_data='main')
    ]
]
cash_text = 'برای ادامه معامله ارز مورد نظر را انتخاب کنید'
cash_keyboard = [
    [
        InlineKeyboardButton("دلار", callback_data='dollar'),
        InlineKeyboardButton("یورو", callback_data='euro'),
        InlineKeyboardButton("پوند", callback_data='pond')
    ],
    [
        InlineKeyboardButton("یوان", callback_data=str('yuan')),
        InlineKeyboardButton("لیر", callback_data=str('leer'))
    ],
    [
        InlineKeyboardButton("↩️بازگشت", callback_data='deal')
    ]
]
crypto_text = 'ارز دیجیتال مورد نظر خود را انتخاب کنید'
crypto_keyboard = [
    [
        InlineKeyboardButton("Bitcoin", callback_data=currency_name['Bitcoin']),
        InlineKeyboardButton("Ethereum", callback_data=currency_name['Ethereum']),
        InlineKeyboardButton("Monero", callback_data=currency_name['Monero']),
    ],
    [
        InlineKeyboardButton("Dash", callback_data=currency_name['Dash']),
        InlineKeyboardButton("Litecoin", callback_data=currency_name['Litecoin']),
        InlineKeyboardButton("Tether", callback_data=currency_name['Tether']),
    ],
    [
        InlineKeyboardButton("Cardano", callback_data=currency_name['Cardano']),
        InlineKeyboardButton('TRON', callback_data=currency_name['TRON'])
    ],
    [
        InlineKeyboardButton("↩️بازگشت", callback_data='deal')
    ]
]
deal_text = '💵 معامله با ما'
wallet_keyboard = [
    [
        InlineKeyboardButton("💵 افزایش موجودی", callback_data='increase'),
        InlineKeyboardButton("💎 برداشت وجه", callback_data='decrease'),
    ],
    [
        InlineKeyboardButton("↩️بازگشت", callback_data='main')
    ]
]
wallet_text = '💳 کیف پول'
wallet_action_keyboard = [
    [
        InlineKeyboardButton("Bitcoin", callback_data=currency_name['Bitcoin']),
        InlineKeyboardButton("Ethereum", callback_data=currency_name['Ethereum']),
        InlineKeyboardButton("Monero", callback_data=currency_name['Monero']),
    ],
    [
        InlineKeyboardButton("Dash", callback_data=currency_name['Dash']),
        InlineKeyboardButton("Litecoin", callback_data=currency_name['Litecoin']),
        InlineKeyboardButton("Tether", callback_data=currency_name['Tether']),
    ],
    [
        InlineKeyboardButton("Cardano", callback_data=currency_name['Cardano']),
        InlineKeyboardButton('TRON', callback_data=currency_name['TRON'])
    ],
    [
        InlineKeyboardButton("💳تومان", callback_data='toman'),
        InlineKeyboardButton("↩️بازگشت", callback_data='wallet')
    ],
]
wallet_action_text = '👈 ارز مورد نظر خود را برای تراکنش مورد نظر انتخاب نمایید: '
market_keyboard = [
    [
        InlineKeyboardButton("↩️بازگشت", callback_data='main')
    ]
]
market_text = '📈 بازارها'
recommend_keyboard = [
    [
        InlineKeyboardButton("↩️بازگشت", callback_data='main')
    ]
]
recommend_text = '💸 معرفی به دوستان'
account_keyboard = [
    [
        InlineKeyboardButton("📱 تایید شماره تلفن", callback_data='phone'),
        InlineKeyboardButton("✅ احراز هویت", callback_data='auth'),
    ],
    [
        InlineKeyboardButton("💳 تکمیل اطلاعات بانکی", callback_data='bank_info'),
        InlineKeyboardButton("↩️بازگشت", callback_data='main')
    ]
]
account_text = '👤 حساب کاربری'
rules_keyboard = [
    [
        InlineKeyboardButton("↩️بازگشت", callback_data='main')
    ]
]
rules_text = rules.rules[0]
service_keyboard = [
    [
        InlineKeyboardButton("↩️بازگشت", callback_data='main')
    ]
]
service_text = '💬 پشتیبانی'

keyboards = {'main': [main_keyboard, main_text],
             'deal': [deal_keyboard, deal_text],
             'wallet': [wallet_keyboard, wallet_text],
             'market': [market_keyboard, market_text],
             'recommend': [recommend_keyboard, recommend_text],
             'account': [account_keyboard, account_text],
             'rules': [rules_keyboard, rules_text],
             'service': [service_keyboard, service_text],
             'cash': [cash_keyboard, cash_text],
             'crypto': [crypto_keyboard, crypto_text],
             'wallet_action': [wallet_action_keyboard, wallet_action_text]}


def get_duration(time: datetime.datetime):
    duration = datetime.datetime.now(datetime.timezone.utc) - time
    mins = duration.seconds // 60
    hours = mins // 60
    return hours, mins - hours * 60, duration.seconds - mins * 60
