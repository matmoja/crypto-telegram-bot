import requests
from telegram import Update
from telegram.ext import CallbackContext

COINGECKO_API_URL = 'https://api.coingecko.com/api/v3/simple/price'


tracked_coins = {}

class CryptoBotHelper:
    @staticmethod
    def start(update: Update, context: CallbackContext) -> None:
        update.message.reply_text('Welcome to the Crypto Bot! Type /help to see the available commands.')

    @staticmethod
    def help_command(update: Update, context: CallbackContext) -> None:
        update.message.reply_text('/start : start the bot\n'
                                  '/help : see commands\n'
                                  '/add <coin> : add coin to tracking list\n'
                                  '/remove <coin> : remove coin from tracking list\n'
                                  '/show : show current coin list\n'
                                  '/fetch : fetch prices of coin list\n'
                                  '/repeat <time interval in min>: send prices automatically after specified interval')

    @staticmethod
    def add_coin(update: Update, context: CallbackContext) -> None:
        coin = context.args[0].upper()
        if coin not in tracked_coins:
            tracked_coins[coin] = None
            update.message.reply_text(f'{coin} added to the tracking list.')
        else:
            update.message.reply_text(f'{coin} is already in the tracking list.')

    @staticmethod
    def remove_coin(update: Update, context: CallbackContext) -> None:
        coin = context.args[0].upper()
        if coin in tracked_coins:
            del tracked_coins[coin]
            update.message.reply_text(f'{coin} removed from the tracking list.')
        else:
            update.message.reply_text(f'{coin} is not in the tracking list.')

    @staticmethod
    def show_list(update: Update, context: CallbackContext) -> None:
        if tracked_coins:
            coin_list = ', '.join(tracked_coins.keys())
            update.message.reply_text(f'Tracked coins: {coin_list}')
        else:
            update.message.reply_text('No coins are currently being tracked.')

    @staticmethod
    def fetch_prices(update: Update, context: CallbackContext) -> None:
        for coin in tracked_coins:
            params = {'ids': coin, 'vs_currencies': 'usd'}
            response = requests.get(COINGECKO_API_URL, params=params)
            data = response.json()

            if coin in data and 'usd' in data[coin]:
                tracked_coins[coin] = data[coin]['usd']

        prices_text = '\n'.join([f'{coin}: ${price}' for coin, price in tracked_coins.items()])
        update.message.reply_text(f'Current prices:\n{prices_text}')

    @staticmethod
    def repeat(update: Update, context: CallbackContext) -> None:
        try:
            interval = int(context.args[0])
            if interval <= 0:
                update.message.reply_text('Interval must be a positive integer.')
                return

            job_context = {'update': update, 'interval': interval * 60}
            job = context.job_queue.run_repeating(CryptoBotHelper.repeat_prices, interval * 60, context=job_context)
            context.user_data['job'] = job

            update.message.reply_text(f'Prices will be sent every {interval} minutes. Type /stop_repeat to stop.')

        except (IndexError, ValueError):
            update.message.reply_text('Invalid command. Please provide a positive integer as the time interval in minutes.')

    @staticmethod
    def stop_repeat(update: Update, context: CallbackContext) -> None:
        if 'job' in context.user_data:
            job = context.user_data['job']
            job.schedule_removal()
            del context.user_data['job']
            update.message.reply_text('Price updates have been stopped.')
        else:
            update.message.reply_text('No price updates are currently scheduled.')

    @staticmethod
    def repeat_prices(context: CallbackContext) -> None:
        job = context.job
        CryptoBotHelper.fetch_prices(job.context['update'], context)
        context.job.interval = job.context['interval']
