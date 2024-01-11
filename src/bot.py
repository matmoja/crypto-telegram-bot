# This code is just for a test to see if bot works instead of the update function

from telegram import Bot, Update
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
from helpers import CryptoBotHelper

TELEGRAM_BOT_TOKEN = '6902442506:AAHe2fCbSNFbENajFaavlLeEL1udJuSIQAk'

def main() -> None:
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    crypto_bot_helper = CryptoBotHelper()

    def handle_messages(update: Update, context) -> None:
        text = update.message.text

        if text.startswith('/start'):
            crypto_bot_helper.start(update, context)
        elif text.startswith('/help'):
            crypto_bot_helper.help_command(update, context)
        elif text.startswith('/add'):
            crypto_bot_helper.add_coin(update, context.args)
        elif text.startswith('/remove'):
            crypto_bot_helper.remove_coin(update, context.args)
        elif text.startswith('/show'):
            crypto_bot_helper.show_list(update, context)
        elif text.startswith('/fetch'):
            crypto_bot_helper.fetch_prices(update, context)
        elif text.startswith('/repeat'):
            crypto_bot_helper.repeat(update, context.args, context.job_queue)
        elif text.startswith('/stop_repeat'):
            crypto_bot_helper.stop_repeat(update, context.job_queue)

    message_handler = MessageHandler(Filters.text & ~Filters.command, handle_messages)
    bot = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    bot.dispatcher.add_handler(message_handler)

    bot.dispatcher.add_handler(CommandHandler("start", crypto_bot_helper.start))
    bot.dispatcher.add_handler(CommandHandler("help", crypto_bot_helper.help_command))
    bot.dispatcher.add_handler(CommandHandler("add", crypto_bot_helper.add_coin, pass_args=True))
    bot.dispatcher.add_handler(CommandHandler("remove", crypto_bot_helper.remove_coin, pass_args=True))
    bot.dispatcher.add_handler(CommandHandler("show", crypto_bot_helper.show_list))
    bot.dispatcher.add_handler(CommandHandler("fetch", crypto_bot_helper.fetch_prices))
    bot.dispatcher.add_handler(CommandHandler("repeat", crypto_bot_helper.repeat, pass_args=True, pass_job_queue=True, pass_chat_data=True))
    bot.dispatcher.add_handler(CommandHandler("stop_repeat", crypto_bot_helper.stop_repeat, pass_chat_data=True))

    bot.start_polling()
    bot.idle()

if __name__ == '__main__':
    main()
