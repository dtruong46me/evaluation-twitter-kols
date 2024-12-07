
import os
import tweepy
import pandas as pd
from typing import List
from dotenv import load_dotenv

load_dotenv()

class TwitterAPI:
    def __init__(self):
        self.api = self.authenticate_twitter()

    def authenticate_twitter(self) -> tweepy.API:
        """
        Authenticate to Twitter API
        """
        API_KEY             = os.getenv("API_KEY")
        API_SECRET_KEY      = os.getenv("API_SECRET_KEY")
        ACCESS_TOKEN        = os.getenv("ACCESS_TOKEN")
        ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

        auth = tweepy.OAuthHandler(consumer_key=API_KEY,
                                   consumer_secret=API_SECRET_KEY)
        
        auth.set_access_token(key=ACCESS_TOKEN, secret=ACCESS_TOKEN_SECRET)

        api = tweepy.API(auth=auth, wait_on_rate_limit=True)

        return api
    

    def scrape_twitter_data(self, usernames: List[str], num_posts: int) -> List[dict]:
        """
        Scrape Twitter data
        """
        data = []
        for username in usernames:
            try:
                tweets = self.api.user_timeline(screen_name=username, count=num_posts, tweet_mode="extended")
                for tweet in tweets:
                    data.append({
                        "username": username,
                        "tweet_id": tweet.id,
                        "created_at": tweet.created_at,
                        "content": tweet.full_text,
                        "likes": tweet.favorite_count,
                        "retweets": tweet.retweet_count,
                        "hashtags": [hashtag['text'] for hashtag in tweet.entities["hashtags"]]
                    })
            except Exception as e:
                print(f"ERROR: Unable to fetch data for {username}. Error: {e}")
        return data