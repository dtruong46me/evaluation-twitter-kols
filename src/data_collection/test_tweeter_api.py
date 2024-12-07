import os
import logging
from typing import List
from dotenv import load_dotenv
import tweepy

load_dotenv()

class TwitterAPI:
    def __init__(self):
        self.client = self.authenticate_twitter()
    

    def authenticate_twitter(self) -> tweepy.Client:
        """
        Authenticate to Twitter API v2
        """
        BEARER_TOKEN = os.getenv("BEARER_TOKEN")

        return tweepy.Client(bearer_token=BEARER_TOKEN)
    

    def search_users_by_keyword(self, keywords: List[str]):
        """
        Search for users by keywords
        Args:
            keywords (List[str]): List of keywords
        Returns:
            List[dict]: List of user information
        """
        usernames = []
        for keyword in keywords:
            try:
                # Search recent tweets using API v2
                response = self.client.search_recent_tweets(query=keyword, tweet_fields=["author_id"], max_results=10)
                
                if response.data:
                    tweets: tweepy.Tweet = response.data
                    for tweet in tweets:
                        tweet_info = tweet.data
                        usernames.append(tweet_info)

            except Exception as e:
                logging.error(f"ERROR: {e}")
                print(e)

        return usernames
    

if __name__ == '__main__':
    twitter = TwitterAPI()
    usernames = twitter.search_users_by_keyword(["data science", "machine learning"])
    print(usernames)