import logging
import currency
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

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
    user = update.message.from_user
    print('start over ', user.username)
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("ارز حواله", callback_data=str(HAVALEH) + ',' + user.username),
            InlineKeyboardButton("ارز دیجیتال", callback_data=str(DIGITAL) + ',' + user.username),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(text="معامله خود را شروع کنید", reply_markup=reply_markup)
    return FIRST


def havaleh(update: Update, context: CallbackContext) -> None:
    print('ARZ HAVALEH')
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("دلار", callback_data=str('dollar')),
            InlineKeyboardButton("یورو", callback_data=str('euro')),
            InlineKeyboardButton("پوند", callback_data=str('pond'))
        ],
        [
            InlineKeyboardButton("یوان", callback_data=str('yuan')),
            InlineKeyboardButton("لیر", callback_data=str('leer'))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="ارز حواله", reply_markup=reply_markup
    )
    return SECOND


def digital(update: Update, context: CallbackContext) -> None:
    print('ARZ DIGITAL')
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()

    keyboard = [
        [
            InlineKeyboardButton("Bitcoin", callback_data=str(currency_name['Bitcoin'])),
            InlineKeyboardButton("Ethereum", callback_data=str(currency_name['Ethereum'])),
            InlineKeyboardButton("Monero", callback_data=str(currency_name['Monero'])),
        ],
        [
            InlineKeyboardButton("Dash", callback_data=str(currency_name['Dash'])),
            InlineKeyboardButton("Litecoin", callback_data=str(currency_name['Litecoin'])),
            InlineKeyboardButton("Tether", callback_data=str(currency_name['Tether'])),
        ],
        [
            InlineKeyboardButton("Cardano", callback_data=str(currency_name['Cardano'])),
            InlineKeyboardButton('TRON', callback_data=str(currency_name['TRON']))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="ارز دیجیتال", reply_markup=reply_markup
    )
    return SECOND


def other(update: Update, context: CallbackContext) -> None:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    print('other: ', query.data.strip('][').split(', '))
    keyboard = [
        [
            InlineKeyboardButton("خرید " + query.data, callback_data=query.data + ' buy'),
            InlineKeyboardButton("فروش " + query.data, callback_data=query.data + ' sell'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="منوی خرید و فروش", reply_markup=reply_markup
    )
    # Transfer to conversation state `SECOND`
    return THIRD


def sell_buy(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    print('SELL BUY: ', query.data)
    keyboard = [
        [
            InlineKeyboardButton(" منوی اصلی ", callback_data=str(ONE)),
            InlineKeyboardButton(" خدانگهدار ", callback_data=str(TWO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="منوی خرید و فروش", reply_markup=reply_markup
    )
    # Transfer to conversation state `SECOND`
    return FIFTH


def end(update: Update, context: CallbackContext) -> None:
    print('END')
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="See you next time!")
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
                CallbackQueryHandler(end, pattern='^' + str(TWO) + '$'),
            ],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    # Add ConversationHandler to dispatcher that will be used for handling
    # updates
    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
