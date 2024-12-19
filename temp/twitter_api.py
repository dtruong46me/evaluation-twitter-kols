
import requests
from utils import load_config

class TwitterAPI:
    def __init__(self):
        self.config = load_config("config/twitter_config.yml")
        self.base_url = "https://api.twitter.com/2/tweets/search/recent"
        self.headers = {
            "Authorization": f"Bearer {self.config['bearer_token']}"
        }

    def fetch_tweets(self):
        params = {
            "query": self.config["query"],
            "max_results": self.config["max_results"]
        }
        response = requests.get(self.base_url, headers=self.headers, params=params)
        tweets = response.json().get("data", [])
        return tweets