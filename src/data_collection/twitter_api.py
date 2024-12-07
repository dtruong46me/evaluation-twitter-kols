
import os
import tweepy
import pandas as pd
from typing import List
from dotenv import load_dotenv

load_dotenv()

class TwitterAPI:
    def __init__(self):
        self.client = self.authenticate_twitter()

    def authenticate_twitter(self) -> tweepy.Client:
        """
        Authenticate to Twitter API v2
        """
        BEARER_TOKEN = os.getenv("BEARER_TOKEN")
        API_KEY = os.getenv("API_KEY")
        API_SECRET_KEY = os.getenv("API_SECRET_KEY")
        ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
        ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

        client = tweepy.Client(bearer_token=BEARER_TOKEN,
                               consumer_key=API_KEY,
                               consumer_secret=API_SECRET_KEY,
                               access_token=ACCESS_TOKEN,
                               access_token_secret=ACCESS_TOKEN_SECRET)
        
        return client
    
    def search_users(self, keyword: str, limit: int) -> List[dict]:
        """
        Search for users based on a keyword
        API: `GET /2/tweets/search/recent`
        Reference: https://developer.x.com/en/docs/x-api/tweets/search/api-reference/get-tweets-search-recent
        """
        try:
            query = f"{keyword} lang:en"
            response = self.client.search_recent_tweets(query=query, max_results=limit, tweet_fields=['author_id'])
            users = []
            for tweet in response.data:
                user_response = self.client.get_user(id=tweet.author_id, user_fields=["username", "public_metrics", "created_at", "description"])
                if user_response.data:
                    users.append(user_response.data)
            return users

        except Exception as e:
            print(f"ERROR1: {e}")
            return []


    def fetch_tweets_by_user(self, user_id: str, limit: int) -> List[dict]:
        """
        Fetch tweets for a specific user
        """
        try:
            response = self.client.get_users_tweets(id=user_id, max_results=limit, tweet_fields=["created_at", "public_metrics", "text"])
            return response.data if response.data else []
        
        except Exception as e:
            print(f"ERROR2: {e}")
            return []

if __name__ == "__main__":
    KEYWORD     = "Web3"
    MAX_RESULTS = 10

    api = TwitterAPI()
    users = api.search_users(keyword=KEYWORD, limit=MAX_RESULTS)
    print(users)
    for user in users:
        tweets = api.fetch_tweets_by_user(user_id=user['id'], limit=5)
        print(tweets, "\n")
        
    
    print("Done!")