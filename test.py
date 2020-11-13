import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


class Money_Bot:
    def __init__(self):
        self.keyboard = [
            [
                InlineKeyboardButton("ارز حواله", callback_data='1'),
                InlineKeyboardButton("ارز دیجیتال", callback_data='2'),
            ],
            [InlineKeyboardButton("HELP", callback_data='3')],
        ]

    def start(self, update: Update, context: CallbackContext) -> None:
        reply_markup = InlineKeyboardMarkup(self.keyboard)
        update.message.reply_text('Please choose:', reply_markup=reply_markup)

    def button(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query

        # CallbackQueries need to be answered, even if no notification to the user is needed
        # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
        query.answer()
        print(query.data)
        query.edit_message_text(text="Selected option: {}".format(query.data))

    def help_command(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_text("Use /start to test this bot.")

    def run(self):
        # Create the Updater and pass it your bot's token.
        # Make sure to set use_context=True to use the new context based callbacks
        # Post version 12 this will no longer be necessary
        token = '1441929878:AAF7R_YIbI9y3hQdGyyeyWUv4LYELA0TOho'
        updater = Updater(token, use_context=True)

        updater.dispatcher.add_handler(CommandHandler('start', self.start))
        updater.dispatcher.add_handler(CallbackQueryHandler(self.button))
        updater.dispatcher.add_handler(CommandHandler('help', self.help_command))

        # Start the Bot
        updater.start_polling()

        # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT
        updater.idle()


if __name__ == '__main__':
    bot = Money_Bot()
    bot.run()
