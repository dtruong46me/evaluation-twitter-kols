import tweepy
import time
import json


class TwitterDataCollector:
    """
    Class to collect Twitter data based on keywords using Tweepy and Twitter API v2.
    Includes automatic handling of API rate limits and data persistence.
    """
    def __init__(self, api_key, api_secret, access_token, access_token_secret, keywords, output_file):
        """
        Initialize the TwitterDataCollector class.
        
        :param api_key: Twitter API Key
        :param api_secret: Twitter API Secret Key
        :param access_token: Twitter Access Token
        :param access_token_secret: Twitter Access Token Secret
        :param keywords: List of keywords for Web3
        :param output_file: JSON file path to save the data
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.keywords = keywords
        self.output_file = output_file
        self.api = self.authenticate()
        self.rate_limit_sleep_time = 15 * 60  # Wait for 15 minutes if rate-limited

    def authenticate(self):
        """
        Authenticate to Twitter API using Tweepy.
        
        :return: Tweepy client object
        """
        try:
            client = tweepy.Client(
                bearer_token=None,  # Optional, only needed for additional features
                consumer_key=self.api_key,
                consumer_secret=self.api_secret,
                access_token=self.access_token,
                access_token_secret=self.access_token_secret
            )
            print("Authentication Successful!")
            return client
        except Exception as e:
            print(f"Authentication Error: {e}")
            raise

    def fetch_tweets(self, max_results=100):
        """
        Fetch tweets matching the specified keywords.
        Handles rate limits and saves data in JSON format.
        
        :param max_results: Number of tweets to fetch per query (max 100 per API v2 request).
        :return: List of collected tweets
        """
        all_tweets = []  # List to store collected tweets
        
        for keyword in self.keywords:
            next_token = None  # For pagination
            print(f"Collecting tweets for keyword: '{keyword}'")
            while True:
                try:
                    # Call the Twitter API
                    response = self.api.search_recent_tweets(
                        query=keyword,
                        tweet_fields=['author_id', 'created_at', 'public_metrics', 'text'],
                        max_results=max_results,
                        next_token=next_token
                    )
                    if response.data:
                        for tweet in response.data:
                            all_tweets.append(tweet.data)

                    # Check if pagination is possible
                    next_token = response.meta.get("next_token")
                    if not next_token:
                        break  # No more tweets to fetch
                    print("Fetching next batch...")

                except tweepy.TooManyRequests as e:
                    print("Rate limit reached. Waiting for quota reset...")
                    time.sleep(self.rate_limit_sleep_time)
                except Exception as e:
                    print(f"An error occurred: {e}")
                    break

        # Save collected data to JSON
        self.save_to_json(all_tweets)
        return all_tweets

    def save_to_json(self, data):
        """
        Save collected tweet data to a JSON file.
        
        :param data: List of tweet dictionaries
        :return: None
        """
        try:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"Data successfully saved to {self.output_file}")
        except Exception as e:
            print(f"Error saving data: {e}")

if __name__ == "__main__":
    # Twitter API credentials (replace with your own credentials)
    API_KEY = "your_api_key"
    API_SECRET = "your_api_secret"
    ACCESS_TOKEN = "your_access_token"
    ACCESS_TOKEN_SECRET = "your_access_token_secret"

    # Keywords for Web3
    KEYWORDS = ["Web3", "DeFi", "NFT", "blockchain", "crypto", "metaverse"]

    # Output file path
    OUTPUT_FILE = "web3_tweets.json"

    # Initialize the collector
    collector = TwitterDataCollector(
        api_key=API_KEY,
        api_secret=API_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET,
        keywords=KEYWORDS,
        output_file=OUTPUT_FILE
    )

