from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
from helpers import CryptoBotHelper

TELEGRAM_BOT_TOKEN = '6902442506:AAHe2fCbSNFbENajFaavlLeEL1udJuSIQAk'

def main() -> None:
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    crypto_bot_helper = CryptoBotHelper()

    def handle_messages(update, context):
        text = update.message.text

        # Check for specific commands or keywords in the text
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
    updater.dispatcher.add_handler(message_handler)

    updater.dispatcher.add_handler(CommandHandler("start", crypto_bot_helper.start))
    updater.dispatcher.add_handler(CommandHandler("help", crypto_bot_helper.help_command))
    updater.dispatcher.add_handler(CommandHandler("add", crypto_bot_helper.add_coin, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler("remove", crypto_bot_helper.remove_coin, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler("show", crypto_bot_helper.show_list))
    updater.dispatcher.add_handler(CommandHandler("fetch", crypto_bot_helper.fetch_prices))
    updater.dispatcher.add_handler(CommandHandler("repeat", crypto_bot_helper.repeat, pass_args=True, pass_job_queue=True, pass_chat_data=True))
    updater.dispatcher.add_handler(CommandHandler("stop_repeat", crypto_bot_helper.stop_repeat, pass_chat_data=True))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
