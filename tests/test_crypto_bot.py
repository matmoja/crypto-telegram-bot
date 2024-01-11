import unittest
from unittest.mock import MagicMock, patch
from telegram.ext import Updater

from crypto_bot import main

class TestCryptoBot(unittest.TestCase):

    @patch('crypto_bot.Updater')
    @patch('crypto_bot.CryptoBotHelper')
    def test_main(self, MockCryptoBotHelper, MockUpdater):
        updater_instance = MockUpdater.return_value
        crypto_bot_helper_instance = MockCryptoBotHelper.return_value

        main()

        MockUpdater.assert_called_once_with(bot=updater_instance.bot)
        MockCryptoBotHelper.assert_called_once_with()

if __name__ == '__main__':
    unittest.main()
