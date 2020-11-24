import logging
import Currency
from telegram import *
from telegram.ext import *
from DBMS import *
from sms import SMS
import unidecode

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# DBMS
database = DBMS()
all_users = database.get_users()

users_dict = {}
for each in all_users:
    users_dict[each[0]] = list(each)
all_users = users_dict
print(all_users)

# Stages
FIRST, SECOND, THIRD, FORTH, FIFTH = range(5)
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

prices = Currency.Currency()

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
        InlineKeyboardButton("📱 تایید شماره تلفن", callback_data='increase'),
        InlineKeyboardButton("✅ احراز هویت", callback_data='decrease'),
    ],
    [
        InlineKeyboardButton("💳 تکمیل اطلاعات بانکی", callback_data='main'),
        InlineKeyboardButton("↩️بازگشت", callback_data='main')
    ]
]
account_text = '👤 حساب کاربری'
rules_keyboard = [
    [
        InlineKeyboardButton("↩️بازگشت", callback_data='main')
    ]
]
rules_text = '⚖️ قوانین'
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
             'crypto': [crypto_keyboard, crypto_text]}


def start(update: Update, context: CallbackContext) -> None:
    person = update.message.from_user
    print('New Thread with ', person.username)
    context.user_data['username'] = person.username

    context.bot.send_message(update.message.chat_id, wellcome_text)
    reply_markup = InlineKeyboardMarkup(main_keyboard)
    update.message.reply_text(main_text, reply_markup=reply_markup)
    return FIRST


def main_menu(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    reply_markup = InlineKeyboardMarkup(main_keyboard)
    query.edit_message_text(main_text, reply_markup=reply_markup)
    return FIRST


def menu_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    reply_markup = InlineKeyboardMarkup(keyboards[query.data][0])
    if query.data == 'market':
        query.edit_message_text('در حال ارزیابی قیمت ها ... ', reply_markup=reply_markup)
        c = Currency.Currency()
        c.get_prices()
        query.edit_message_text(c.post_reporter(), reply_markup=reply_markup)
    elif query.data == 'cash' or query.data == 'crypto':
        context.user_data['d_type'] = query.data
        query.edit_message_text(keyboards[query.data][1], reply_markup=reply_markup)
        return SECOND
    else:
        query.edit_message_text(keyboards[query.data][1], reply_markup=reply_markup)
    return FIRST


def deal_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("💎خرید از ما ", callback_data='buy'),
            InlineKeyboardButton("💎فروش به ما ", callback_data='sell'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if query.data == 'deal':
        reply_markup = InlineKeyboardMarkup(keyboards[query.data][0])
        query.edit_message_text(keyboards[query.data][1], reply_markup=reply_markup)
        return FIRST
    else:
        query.edit_message_text(
            text="منوی خرید و فروش", reply_markup=reply_markup)
        context.user_data['currency'] = query.data
        return THIRD


def amount(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    context.user_data['T_type'] = query.data
    c = Currency.Currency()
    if context.user_data['d_type'] == 'crypto':
        if query.data == 'buy':
            query.edit_message_text(text="در حال محاسبه قیمت")
            c.get_prices()
            c.minimum_calc()
            query.edit_message_text(text=c.minimum_reporter(context.user_data['currency'], True))
            context.user_data['unit'] = c.min_prices
        else:
            query.edit_message_text(text="در حال محاسبه قیمت")
            c.get_prices()
            c.minimum_calc()
            query.edit_message_text(text=c.minimum_reporter(context.user_data['currency'], False))
            context.user_data['unit'] = c.min_prices
    return THIRD


def transaction(update: Update, context: CallbackContext) -> None:
    print(update.message.text, context.user_data)
    unit = float(unidecode.unidecode(update.message.text))
    unit *= context.user_data['unit'][0]
    keyboard = [
        [
            InlineKeyboardButton(" تایید ", callback_data='yes'),
            InlineKeyboardButton(" لغو ", callback_data='no'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if context.user_data['unit'][2] < unit:
        update.message.reply_text(text=f'هزینه معامله شما برابر : {unit} تومان' + context.user_data['currency'],
                                  reply_markup=reply_markup)
        context.user_data['unit'] = unit
    else:
        update.message.reply_text(text='مقدار وارد شده کمتر از حد معاملات است',
                                  reply_markup=reply_markup)
    return FORTH


def make_deal(update: Update, context: CallbackContext) -> None:
    print(context.user_data)
    pass


def look_up(username):
    global all_users
    if username in all_users:
        return True
    else:
        return False


def authenticate(update: Update, context: CallbackContext) -> None:
    user = User(context.user_data['username'], context.user_data['phone'])
    print(unidecode.unidecode(update.message.text))
    if unidecode.unidecode(update.message.text) == context.user_data['v_code']:
        user.is_auth = True
        print('User Authenticated')
        users_dict[user.get_data_inlist()[0]] = user.get_data_inlist()
        reply_markup = InlineKeyboardMarkup(main_keyboard)
        update.message.reply_text(main_text, reply_markup=reply_markup)
        return FIRST
    else:
        return SECOND


def sign_up(update: Update, context: CallbackContext) -> None:
    person = update.message.from_user
    print("Phone of {}: {}".format(person.first_name, update.message.text))
    update.message.reply_text("پس از دریافت پیامک کد تایید را وارد نمایید:")
    sms_api = SMS()
    code = sms_api.send(update.message.text)
    context.user_data['v_code'] = code
    context.user_data['phone'] = update.message.text
    return SECOND


def start_over(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("ارز حواله", callback_data=str(HAVALEH)),
            InlineKeyboardButton("ارز دیجیتال", callback_data=str(DIGITAL)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(text="معامله خود را شروع کنید", reply_markup=reply_markup)
    return FIRST


def cash(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    print('ARZ HAVALEH ', query.data)

    keyboard = [
        [
            InlineKeyboardButton("دلار", callback_data='dollar'),
            InlineKeyboardButton("یورو", callback_data='euro'),
            InlineKeyboardButton("پوند", callback_data='pond')
        ],
        [
            InlineKeyboardButton("یوان", callback_data=str('yuan')),
            InlineKeyboardButton("لیر", callback_data=str('leer'))
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="برای ادامه معامله ارز مورد نظر را انتخاب کنید", reply_markup=reply_markup
    )
    return THIRD


def crypto(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    print('ارز دیجیتال مورد نظر خود را انتخاب کنید: ', query.data)

    keyboard = [
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
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="اارز دیجیتال مورد نظر خود را انتخاب کنید: ", reply_markup=reply_markup
    )
    return THIRD


def other(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    print('other: ', query.data)
    keyboard = [
        [
            InlineKeyboardButton("خرید از ما ", callback_data='buy'),
            InlineKeyboardButton("فروش به ما ", callback_data='sell'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="منوی خرید و فروش", reply_markup=reply_markup
    )
    context.user_data['currency'] = query.data
    return THIRD


def end(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text='به امید دیدار')
    return ConversationHandler.END


def main():
    updater = Updater("1441929878:AAF7R_YIbI9y3hQdGyyeyWUv4LYELA0TOho")
    dispatcher = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FIRST: [
                CallbackQueryHandler(main_menu, pattern='^' + 'main' + '$'),
                CallbackQueryHandler(menu_handler, pattern='^' + '.+' + '$'),

            ],
            SECOND: [
                CallbackQueryHandler(deal_handler, pattern='^' + '.+' + '$')
            ],
            THIRD: [
                CallbackQueryHandler(amount, pattern='^buy$|^sell$'),
                MessageHandler(Filters.regex('^.+$'), transaction),
            ],
            FORTH: [
                CallbackQueryHandler(make_deal, pattern='^yes$'),
                CallbackQueryHandler(end, pattern='^no$'),
            ],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    dispatcher.add_handler(conv_handler)
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
"""CallbackQueryHandler(test, pattern='^' + 'wallet' + '$'),
                CallbackQueryHandler(test, pattern='^' + 'market' + '$'),
                CallbackQueryHandler(test, pattern='^' + 'recommend' + '$'),
                CallbackQueryHandler(test, pattern='^' + 'account' + '$'),
                CallbackQueryHandler(test, pattern='^' + 'rules' + '$'),
                CallbackQueryHandler(test, pattern='^' + 'service' + '$'),
                
                
                CallbackQueryHandler(other, pattern='^.*$'),

                MessageHandler(Filters.regex('^\d{11}\d*$'), sign_up),
                MessageHandler(Filters.regex('^\d{1,5}$'), authenticate)
                """