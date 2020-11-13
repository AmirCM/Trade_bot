import logging
from telegram import *
from telegram.ext import *

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

token = '1441929878:AAF7R_YIbI9y3hQdGyyeyWUv4LYELA0TOho'


def start(update: Update, context: CallbackContext):
    """send hello msg"""

    print(context)
    print(update)
    update.message.delete()
    with open('hello.txt', mode='r', encoding='UTF-8') as file:
        txt = file.read()
    context.bot.send_message(update.message.chat_id, txt)


def bot():
    updater = Updater(token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    bot()
