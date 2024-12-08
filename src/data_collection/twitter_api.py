
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


        # """
        # PS C:\Users\dnhtr\DT_Projects\evaluation-twitter-kols> & C:/Users/dnhtr/AppData/Local/Programs/Python/Python310/python.exe c:/Users/dnhtr/DT_Projects/evaluation-twitter-kols/src/data_collection/twitter_api.py
        # Keywords: ['web3', 'blockchain', 'ethereum', 'decentralized', 'crypto', 'nft', 'metaverse', 'defi', 'dapp', 'smart contract', 'solidity']
        # Search results for 'web3':
        # [
        #     {
        #         'id': 1865780476398522837, 
        #         'text': 'Web3 is redefining value storage and transfer protocols', 
        #         'author_id': 1850283248934408193, 
        #         'created_at': datetime.datetime(2024, 12, 8, 15, 28, 24, tzinfo=datetime.timezone.utc), 
        #         'public_metrics': {
        #             'retweet_count': 0, 
        #             'reply_count': 0, 
        #             'like_count': 0, 
        #             'quote_count': 0, 
        #             'bookmark_count': 0, 
        #             'impression_count': 0
        #         }
        #     }, 
        #     {
        #         'id': 1865780475266302069, 
        #         'text': "Web3's hidden gem: protocols that let users farm yield without risking a fortune", 
        #         'author_id': 1847209958699622400, 
        #         'created_at': datetime.datetime(2024, 12, 8, 15, 28, 24, tzinfo=datetime.timezone.utc), 
        #         'public_metrics': {
        #             'retweet_count': 0, 
        #             'reply_count': 0, 
        #             'like_count': 0, 
        #             'quote_count': 0, 
        #             'bookmark_count': 0, 
        #             'impression_count': 0
        #         }
        #     }, 
        #     {
        #         'id': 1865780474834190583, 
        #         'text': 'RT @ChainbaseHQ: The Chainbase AVS Mainnet is officially live!\n\nThis marks a huge milestone in decentralized data infrastructure. Let’s bre…', 
        #         'author_id': 2781133702, 
        #         'created_at': datetime.datetime(2024, 12, 8, 15, 28, 24, tzinfo=datetime.timezone.utc), 
        #         'public_metrics': {
        #             'retweet_count': 65700, 
        #             'reply_count': 0, 
        #             'like_count': 0, 
        #             'quote_count': 0, 
        #             'bookmark_count': 0, 
        #             'impression_count': 0
        #         }
        #     }, 
        #     {
        #         'id': 1865780473689206905, 
        #         'text': 'RT @TheAureliya: @cz_binance @RonghuiGu @nikichain Just watched this video— \n\n@CertiK audits always give me extra confidence in a project!…', 
        #         'author_id': 1865271618152599552, 
        #         'created_at': datetime.datetime(2024, 12, 8, 15, 28, 24, tzinfo=datetime.timezone.utc), 
        #         'public_metrics': {
        #             'retweet_count': 625, 
        #             'reply_count': 0, 
        #             'like_count': 0, 
        #             'quote_count': 0, 
        #             'bookmark_count': 0, 
        #             'impression_count': 0
        #         }
        #     }, 
        #     {
        #         'id': 1865780473085010159, 
        #         'text': "Web3's hidden gem is its ability to democratize access to financial resources for underserved communities worldwide", 
        #         'author_id': 1838161164770988032, 
        #         'created_at': datetime.datetime(2024, 12, 8, 15, 28, 23, tzinfo=datetime.timezone.utc), 
        #         'public_metrics': {
        #             'retweet_count': 0, 
        #             'reply_count': 0, 
        #             'like_count': 0, 
        #             'quote_count': 0, 
        #             'bookmark_count': 0, 
        #             'impression_count': 0
        #         }
        #     }, 
        #     {
        #         'id': 1865780472338657675, 
        #         'text': 'RT @TheAureliya: @cz_binance @RonghuiGu @nikichain Just watched this video— \n\n@CertiK audits always give me extra confidence in a project!…', 
        #         'author_id': 1643137983967789056, 
        #         'created_at': datetime.datetime(2024, 12, 8, 15, 28, 23, tzinfo=datetime.timezone.utc), 
        #         'public_metrics': {
        #             'retweet_count': 625, 
        #             'reply_count': 0, 
        #             'like_count': 0, 
        #             'quote_count': 0, 
        #             'bookmark_count': 0, 
        #             'impression_count': 0
        #         }
        #     }, 
        #     {
        #         'id': 1865780471151411618, 
        #         'text': "@Web3_Dad I'm interested", 
        #         'author_id': 1073177936700866561, 
        #         'created_at': datetime.datetime(2024, 12, 8, 15, 28, 23, tzinfo=datetime.timezone.utc), 
        #         'public_metrics': {
        #             'retweet_count': 0, 
        #             'reply_count': 0, 
        #             'like_count': 0, 
        #             'quote_count': 0, 
        #             'bookmark_count': 0, 
        #             'impression_count': 0
        #         }
        #     }, 
        #     {
        #         'id': 1865780470799348022, 
        #         'text': 'RT @bunniefied: 👉 Sign up today and be part of the MEET48 revolution!\xa0🚀🚀\n\n✅ Follow @meet_48\n✅ RT &amp; LIKE\n\nWhat is MEET48? 🤔\nMEET48 is an imm…', 
        #         'author_id': 1849071844323983360, 
        #         'created_at': datetime.datetime(2024, 12, 8, 15, 28, 23, tzinfo=datetime.timezone.utc), 
        #         'public_metrics': {
        #             'retweet_count': 300, 
        #             'reply_count': 0, 
        #             'like_count': 0, 
        #             'quote_count': 0, 
        #             'bookmark_count': 0, 
        #             'impression_count': 0
        #         }
        #     }, 
        #     {
        #         'id': 1865780470761332969, 
        #         'text': "Web3's hidden gems are quietly disrupting traditional banking models one protocol at a time", 
        #         'author_id': 1853048986271109121, 
        #         'created_at': datetime.datetime(2024, 12, 8, 15, 28, 23, tzinfo=datetime.timezone.utc), 
        #         'public_metrics': {
        #             'retweet_count': 0, 
        #             'reply_count': 0, 
        #             'like_count': 0, 
        #             'quote_count': 0, 
        #             'bookmark_count': 0, 
        #             'impression_count': 0}}, {'id': 1865780469130039752, 'text': 'RT @CryptoDa_Bless: 🚨ThrillingERROR2: 429 Too Many Requests
        # Too Many Requests
        # User info:
        # {}
        # Recent tweets from the user:
        # [{'id': 1865780476398522837, 'text': 'Web3 is redefining value storage and transfer protocols', 'created_at': datetime.datetime(2024, 12, 8, 15, 28, 24, tzinfo=datetime.timezone.utc), 'public_metrics': {'retweet_count': 0, 'reply_count': 0, 'like_count': 0, 'quote_count': 0, 'bookmark_count': 0, 'impression_count': 0}}, {'id': 1865734629350604927, 'text': 'DeFi protocols are like bridges connecting traditional assets to a world of limitless possibilities', 'created_at': datetime.datetime(2024, 12, 8, 12, 26, 13, tzinfo=datetime.timezone.utc), 'public_metrics': {'retweet_count': 0, 'reply_count': 0, 'like_count': 0, 'quote_count': 0, 'bookmark_count': 0, 'impression_count': 0}}, {'id': 1864670678680473901, 'text': 'Decentralized dreams are made of protocol layers and tokenomics', 'created_at': datetime.datetime(2024, 12, 5, 13, 58, 28, tzinfo=datetime.timezone.utc), 'public_metrics': {'retweet_count': 0, 'reply_count': 0, 'like_count': 0, 'quote_count': 0, 'bookmark_count': 0, 'impression_count': 3}}, {'id': 1863899211709796361, 'text': "Crypto's hidden gem: yield farming platforms that let users lend and borrow assets, generating passive income without ever touching a keyboard", 'created_at': datetime.datetime(2024, 12, 3, 10, 52, 56, tzinfo=datetime.timezone.utc), 'public_metrics': {'retweet_count': 0, 'reply_count': 0, 'like_count': 0, 'quote_count': 0, 'bookmark_count': 0, 'impression_count': 1}}, {'id': 1861713258157142494, 'text': "Crypto's silent revolution: democratizing access to capital and opportunities for all", 'created_at': datetime.datetime(2024, 11, 27, 10, 6, 44, tzinfo=datetime.timezone.utc), 'public_metrics': {'retweet_count': 0, 'reply_count': 0, 'like_count': 0, 'quote_count': 0, 'bookmark_count': 0, 'impression_count': 5}}, {'id': 1858742072406155723, 'text': 'Smart contracts are like magic spells that execute automatically on Ethereum, freeing us from the need for intermediaries and unlocking new possibilities', 'created_at': datetime.datetime(2024, 11, 19, 5, 20, 18, tzinfo=datetime.timezone.utc), 'public_metrics': {'retweet_count': 0, 'reply_count': 0, 'like_count': 0, 'quote_count': 0, 'bookmark_count': 0, 'impression_count': 8}}]

        # """