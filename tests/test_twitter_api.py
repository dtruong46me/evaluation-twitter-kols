import unittest
from unittest.mock import patch
from src.twitter_api.twitter_api import TwitterAPI

class TestTwitterAPI(unittest.TestCase):
    @patch("src.twitter_api.requests.get")
    def test_fetch_tweets(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.json.return_value = {"data": [{"id": "1", "text": "test tweet"}]}
        twitter_api = TwitterAPI()
        tweets = twitter_api.fetch_tweets()
        self.assertEqual(len(tweets), 1)
        self.assertEqual(tweets[0]["text"], "test tweet")

if __name__ == "__main__":
    unittest.main()