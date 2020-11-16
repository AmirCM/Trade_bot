import logging
import currency
from telegram import *
from telegram.ext import *
from DBMS import *

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
    users_dict[each[0]] = each
all_users = users_dict
print(all_users)

# Stages
FIRST, SECOND, THIRD, FORTH, FIFTH = range(5)
# Callback data
ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN = range(7)

HAVALEH, DIGITAL = range(2)
currency_name = {'Bitcoin': 'BTC',
                 'Ethereum': 'ETH',
                 'Monero': 'XMR',
                 'Dash': 'DASH',
                 'Litecoin': 'LTC',
                 'Tether': 'USDT',
                 'Cardano': 'ADA',
                 'TRON': 'TRX'}
prices = currency.Currency()


def look_up(username):
    global all_users
    if username in all_users:
        return True
    else:
        return False


def authenticate(user: User, update: Update):
    print('AUTH', user.username)


def sign_up(update: Update, context: CallbackContext) -> None:
    person = update.message.from_user
    print("Phone of {}: {}".format(person.first_name, update.message.text))
    print(update.message.text)
    keyboard = [
        [
            InlineKeyboardButton("ارز حواله", callback_data=str(HAVALEH) + ',' + person.username),
            InlineKeyboardButton("ارز دیجیتال", callback_data=str(DIGITAL) + ',' + person.username),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("معامله خود را شروع کنید", reply_markup=reply_markup)
    return THIRD


def start(update: Update, context: CallbackContext) -> None:
    print('start')

    person = update.message.from_user

    if look_up(person.username):
        print('User {} already exist'.format(person.username))
        keyboard = [
            [
                InlineKeyboardButton("ارز حواله", callback_data=str(HAVALEH) + ',' + person.username),
                InlineKeyboardButton("ارز دیجیتال", callback_data=str(DIGITAL) + ',' + person.username),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("معامله خود را شروع کنید", reply_markup=reply_markup)
        return FIRST
    else:
        print('New user: ', person.username)
        update.message.reply_text("شماره تلفن خود را وارد نمایید")
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


def havaleh(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    print('ARZ HAVALEH ', query.data)

    keyboard = [
        [
            InlineKeyboardButton("دلار", callback_data='dollar,' + query.data),
            InlineKeyboardButton("یورو", callback_data='euro,' + query.data),
            InlineKeyboardButton("پوند", callback_data='pond,' + query.data)
        ],
        [
            InlineKeyboardButton("یوان", callback_data=str('yuan,' + query.data)),
            InlineKeyboardButton("لیر", callback_data=str('leer,' + query.data))
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="ارز حواله", reply_markup=reply_markup
    )
    return THIRD


def digital(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    print('ارز دیجیتال مورد نظر خود را انتخاب کنید: ', query.data)

    keyboard = [
        [
            InlineKeyboardButton("Bitcoin", callback_data=currency_name['Bitcoin'] + ',' + query.data),
            InlineKeyboardButton("Ethereum", callback_data=currency_name['Ethereum'] + ',' + query.data),
            InlineKeyboardButton("Monero", callback_data=currency_name['Monero'] + ',' + query.data),
        ],
        [
            InlineKeyboardButton("Dash", callback_data=currency_name['Dash'] + ',' + query.data),
            InlineKeyboardButton("Litecoin", callback_data=currency_name['Litecoin'] + ',' + query.data),
            InlineKeyboardButton("Tether", callback_data=currency_name['Tether'] + ',' + query.data),
        ],
        [
            InlineKeyboardButton("Cardano", callback_data=currency_name['Cardano'] + ',' + query.data),
            InlineKeyboardButton('TRON', callback_data=currency_name['TRON'] + ',' + query.data)
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="ارز دیجیتال", reply_markup=reply_markup
    )
    return THIRD


def other(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    print('other: ', query.data)
    keyboard = [
        [
            InlineKeyboardButton("خرید ", callback_data='buy,' + query.data),
            InlineKeyboardButton("فروش ", callback_data='sell,' + query.data),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="منوی خرید و فروش", reply_markup=reply_markup
    )
    return THIRD


def sell_buy(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    print('SELL BUY: ', query.data)
    keyboard = [
        [
            InlineKeyboardButton(" منوی اصلی ", callback_data=str(ONE)),
            InlineKeyboardButton(" خدانگهدار ", callback_data=query.data),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="منوی خرید و فروش", reply_markup=reply_markup
    )
    return FIFTH


def end(update: Update, context: CallbackContext) -> None:
    print('END')
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=query.data)
    return ConversationHandler.END


def main():
    updater = Updater("1441929878:AAF7R_YIbI9y3hQdGyyeyWUv4LYELA0TOho")
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FIRST: [
                CallbackQueryHandler(havaleh, pattern='^' + str(HAVALEH) + ',.*' + '$'),
                CallbackQueryHandler(digital, pattern='^' + str(DIGITAL) + ',.*' + '$'),
            ],
            SECOND: [
                MessageHandler(Filters.regex('^\d{11}\d*$'), sign_up)
            ],
            THIRD: [
                CallbackQueryHandler(other, pattern='^.*$')
            ],
            FORTH: [
                CallbackQueryHandler(sell_buy, pattern='^.*$'),
            ],
            FIFTH: [
                CallbackQueryHandler(start_over, pattern='^' + str(ONE) + '$'),
                CallbackQueryHandler(end, pattern='^.*$'),
            ],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    dispatcher.add_handler(conv_handler)
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
