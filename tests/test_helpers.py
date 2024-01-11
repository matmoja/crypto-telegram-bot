import unittest
from unittest.mock import MagicMock, patch
from telegram import Update
from telegram.ext import CallbackContext, JobQueue

from src.helpers import CryptoBotHelper

class TestCryptoBotHelper(unittest.TestCase):

    def setUp(self):
        self.crypto_bot_helper = CryptoBotHelper()

    @patch('helper.requests.get')
    def test_fetch_prices(self, mock_requests_get):
        mock_update = MagicMock(spec=Update)
        mock_context = MagicMock(spec=CallbackContext)
        mock_job_queue = MagicMock(spec=JobQueue)
        mock_context.job_queue = mock_job_queue

        self.crypto_bot_helper.fetch_prices(mock_update, mock_context)

if __name__ == '__main__':
    unittest.main()
