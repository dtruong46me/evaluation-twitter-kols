
import tweepy
import os, sys
from typing import List, Dict, Any
from dotenv import load_dotenv

path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, path)
from utils import load_config

load_dotenv()

class TwitterAPI:
    def __init__(self):
        self.client = self.authenticate_twitter()

    def authenticate_twitter(self):
        """
        Authenticate to Twitter API V2
        """
        try:
            BEARER_TOKEN = os.getenv("BEARER_TOKEN")

            return tweepy.Client(bearer_token=BEARER_TOKEN)
        
        except Exception as e:
            print(f"ERROR0: {e}")
    
    def search_tweets(self, query: str, max_results: int=10) -> List[Dict[str, Any]]:
        """
        Search for recent tweets based on a query
        Args:
            query (str): search query
            max_results (int): maximum number of results to return
        Returns:
            List of dictionaries containing tweet information
        """
        try:
            # `GET /2/tweets/search/recent` endpoint -> 450 requests per 15-minute window (app auth)
            response = self.client.search_recent_tweets(
                query=query,
                tweet_fields=["id", "text", "author_id", "created_at", "public_metrics"],
                expansions=["author_id"],
                max_results=max_results
            )

            tweets = []
            for tweet in response.data:
                tweets.append({
                    "id": tweet["id"],
                    "text": tweet["text"],
                    "author_id": tweet["author_id"],
                    "created_at": tweet["created_at"],
                    "public_metrics": tweet["public_metrics"]
                })
        
            return tweets

        except Exception as e:
            print(f"ERROR1: {e}")
    
    def get_user_info(self, user_id: str) -> Dict[str, Any]:
        """
        Retrieve user information by User ID
        Args:
            user_id (str): User ID
        Returns:
            Dictionary containing user information
        """
        try:
            response = self.client.get_user(
                id=user_id,
                user_fields=["id", "username", "name", "public_metrics", "description", "created_at"]
            )
        
            user = response.data
            return {
                "id": user["id"],
                "username": user["username"],
                "name": user["name"],
                "followers_count": user["public_metrics"]["followers_count"],
                "following_count": user["public_metrics"]["following_count"],
                "tweet_count": user["public_metrics"]["tweet_count"],
                "listed_count": user["public_metrics"]["listed_count"],
                "description": user["description"],
                "created_at": user["created_at"]
            }

        except Exception as e:
            print(f"ERROR2: {e}")
            return {}
        

    def get_user_tweets(self, user_id: str, max_results: int=10) -> List[Dict[str, Any]]:
        """
        Retrieve recent tweets from a specific user
        Args:
            user_id (str): User ID
            max_results (int): maximum number of results to return
        Returns:
            List of dictionaries containing tweet information
        """
        try:
            response = self.client.get_users_tweets(
                id=user_id,
                tweet_fields=["id", "text", "created_at", "public_metrics"],
                max_results=max_results
            )

            tweets = []
            for tweet in response.data:
                tweets.append({
                    "id": tweet["id"],
                    "text": tweet["text"],
                    "created_at": tweet["created_at"],
                    "public_metrics": tweet["public_metrics"]
                })
            
            return tweets
        
        except Exception as e:
            print(f"ERROR3: {e}")
            return []

if __name__ == "__main__":
    config = load_config()
    keywords = config["twitter"]["keywords"]
    # Output: ['web3', 'blockchain', 'ethereum', 'decentralized', 'crypto', 'nft', 'metaverse', 'defi', 'dapp', 'smart contract', 'solidity']
    print(f"Keywords: {keywords}")

    # Initialize TwitterAPI
    twitterapi = TwitterAPI()

    # Search for recent tweets based on the first keyword
    query = keywords[0]
    tweets = twitterapi.search_tweets(query=query, max_results=10)
    print(f"Search results for '{query}':")
    print(tweets)

    # Collect user info from the first tweet's author
    if tweets:
        first_author_id = tweets[0]["author_id"]
        user_info = twitterapi.get_user_info(user_id=first_author_id)
        print(f"User info:")
        print(user_info)

        # Collect recent tweets from the first author
        user_tweets = twitterapi.get_user_tweets(user_id=first_author_id, max_results=10)
        print(f"Recent tweets from the user:")
        print(user_tweets)