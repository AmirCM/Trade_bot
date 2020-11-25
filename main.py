import logging
import Currency
from telegram.ext import *
from DBMS import *
from sms import SMS
import unidecode
from bot_info import *

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

prices = Currency.Currency()


def start(update: Update, context: CallbackContext) -> None:
    person = update.message.from_user
    print(f' New Thread with {person.username} at : {get_duration(update.message.date)} ago')
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
    if query.data == 'phone':
        query.edit_message_text('👈 شماره همراه خود را وارد کنید:')
        return FIFTH
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
    elif query.data == 'rules':
        query.edit_message_text(keyboards[query.data][1], reply_markup=reply_markup)
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
            context.user_data['unit'] = c.min_prices[context.user_data['currency']]
        else:
            query.edit_message_text(text="در حال محاسبه قیمت")
            c.get_prices()
            c.minimum_calc()
            query.edit_message_text(text=c.minimum_reporter(context.user_data['currency'], False))
            context.user_data['unit'] = c.min_prices[context.user_data['currency']]
    return THIRD


def transaction(update: Update, context: CallbackContext) -> None:
    print(update.message.text, context.user_data)
    unit = float(unidecode.unidecode(update.message.text))
    unit = int(unit * context.user_data['unit'][0])

    keyboard = [
        [
            InlineKeyboardButton(" تایید ", callback_data='yes'),
            InlineKeyboardButton(" لغو ", callback_data='no'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    c_type = context.user_data['currency']
    if context.user_data['unit'][2] < unit:
        update.message.reply_text(
            text=f'هزینه معامله ارز {persian[c_type]} شما برابر : {Currency.separator_int(unit)} تومان',
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
    code = unidecode.unidecode(update.message.text)
    print(code)

    if code == context.user_data['v_code']:
        print('User Authenticated')
        update.message.reply_text('✅ شماره ی شما با موفقیت تایید و ثبت شد')
        return FIRST
    else:
        print('User Not Authenticated')
        update.message.reply_text('❌ کد ارسالی مطابقت ندارد ❌')
        return SECOND


def sign_up(update: Update, context: CallbackContext) -> None:
    person = update.message.from_user
    phone = unidecode.unidecode(update.message.text)

    print("Phone of {}: {}".format(person.first_name, phone))
    keyboard = [
        [
            InlineKeyboardButton("📥ارسال مجدد", callback_data='retry'),
            InlineKeyboardButton("↩️بازگشت", callback_data='account')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("پس از دریافت پیامک کد تایید وارد نمایید: ", reply_markup=reply_markup)
    sms_api = SMS()
    code = sms_api.send(update.message.text)
    context.user_data['v_code'] = code
    context.user_data['phone'] = phone
    return FIFTH


def wrong_input(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(text="در وارد کردن یا صحت شماره خطایی صورت گرفته فرآیند لغو گردید")
    return FIRST


def start_over(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    reply_markup = InlineKeyboardMarkup(main_keyboard)
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
            FIFTH: [
                MessageHandler(Filters.regex('(^(\+98)\d{10}$)|(^\d{11}$)'), sign_up),
                MessageHandler(Filters.regex('^\d{1,5}$'), authenticate),
                MessageHandler(Filters.regex('^.+$'), wrong_input)
            ]
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
