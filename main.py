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

# Stages
FIRST, SECOND, THIRD, FIFTH = range(4)
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


def sign_up(username: str, phone_num: str):
    if not database.get_user(username):
        print('User {} already exist'.format(username))
    else:
        user = User(username, phone_num)
        database.insert_user(user)


def start(update: Update, context: CallbackContext) -> None:
    print('start')

    user = update.message.from_user
    print('id: ', user.username)

    keyboard = [
        [
            InlineKeyboardButton("ارز حواله", callback_data=str(HAVALEH) + ',' + user.username),
            InlineKeyboardButton("ارز دیجیتال", callback_data=str(DIGITAL) + ',' + user.username),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("معامله خود را شروع کنید", reply_markup=reply_markup)

    return FIRST


def start_over(update: Update, context: CallbackContext) -> None:
    print('start over ', user.username)
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
    return SECOND


def digital(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    print('ARZ DIGITAL ', query.data)

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
    return SECOND


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
                CallbackQueryHandler(other, pattern='^.*$')
            ],
            THIRD: [
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
