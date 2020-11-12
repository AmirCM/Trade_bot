from telegram.ext import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Update


############################### Bot ############################################
def start(update: Update, context: CallbackContext):
    update.message.reply_text(main_menu_message(),
                              reply_markup=main_menu_keyboard())


def main_menu(update: Update, context: CallbackContext):
    query = update.callback_query
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          text=main_menu_message(),
                          reply_markup=main_menu_keyboard())


def first_menu(update: Update, context: CallbackContext):
    query = update.callback_query
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          text=first_menu_message(),
                          reply_markup=first_menu_keyboard())


def second_menu(update: Update, context: CallbackContext):
    query = update.callback_query
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          text=second_menu_message(),
                          reply_markup=second_menu_keyboard())


# and so on for every callback_data option
def first_submenu(bot, update):
    pass


def second_submenu(bot, update):
    pass


############################ Keyboards #########################################
def main_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Option 1', callback_data='m1')],
                [InlineKeyboardButton('Option 2', callback_data='m2')],
                [InlineKeyboardButton('...', callback_data='m3')]]
    return InlineKeyboardMarkup(keyboard)


def first_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Submenu 1-1', callback_data='m1_1')],
                [InlineKeyboardButton('Submenu 1-2', callback_data='m1_2')],
                [InlineKeyboardButton('Main menu', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)


def second_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Submenu 2-1', callback_data='m2_1')],
                [InlineKeyboardButton('Submenu 2-2', callback_data='m2_2')],
                [InlineKeyboardButton('Main menu', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)


############################# Messages #########################################
def main_menu_message():
    return 'Choose the option in main menu:'


def first_menu_message():
    return 'Choose the submenu in first menu:'


def second_menu_message():
    return 'Choose the submenu in second menu:'


############################# Handlers #########################################
token = '1441929878:AAF7R_YIbI9y3hQdGyyeyWUv4LYELA0TOho'


updater = Updater(token)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CallbackQueryHandler(main_menu, pattern='main'))
dispatcher.add_handler(CallbackQueryHandler(first_menu, pattern='m1'))
dispatcher.add_handler(CallbackQueryHandler(second_menu, pattern='m2'))
dispatcher.add_handler(CallbackQueryHandler(first_submenu,
                                            pattern='m1_1'))
dispatcher.add_handler(CallbackQueryHandler(second_submenu,
                                            pattern='m2_1'))

updater.start_polling()
################################################################################
