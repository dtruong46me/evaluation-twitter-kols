import os
import sys
import time
import pandas as pd
from typing import List, Dict, Any

root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, root)

from src.data_collection.kafka.utils import *
from src.data_collection.kafka.utils import *
#from settings import KAFKA_ADDRESS
from src.data_collection.kafka.json_producer import setting_up
from src.data_collection.kafka.twitter_api import TwitterAPI
from src.utils import load_config


def get_web3_users_info(twitter_api: TwitterAPI, keywords: List[str], max_tweets_per_keyword: int = 50) -> List[Dict[str, Any]]:
    """
    Fetch user information for individuals involved in the Web3 space.

    Args:
        twitter_api (TwitterAPI): An instance of the TwitterAPI class.
        keywords (List[str]): List of keywords related to Web3 topics.
        max_tweets_per_keyword (int): Maximum number of tweets to fetch per keyword.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing user information.
    """
    user_info_list = []
    tweets_list = []
    for keyword in keywords:
        print(f"Searching tweets for keyword: {keyword}")
        try:
            tweets = twitter_api.search_tweets(query=keyword, max_results=max_tweets_per_keyword)
            tweets_list.extend(tweets)

            for tweet in tweets:
                user_id = tweet["author_id"]
                user_info = twitter_api.get_user_info(user_id=user_id)
                if user_info:  # Check if user info is valid
                    user_info_list.append(user_info)
        except Exception as e:
            print(f"Error while processing keyword '{keyword}': {e}")

    return user_info_list, tweets_list

if __name__ == "__main__":
    ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    config = load_config()
    keywords = config["twitter"]["keywords"] # List of Web3-related keywords
    
    twitter_api = TwitterAPI()
    print("Fetching Web3 user information...")
    kafka_config = read_config()

    tweet_producer = setting_up(config=kafka_config, topic="twitter_tweets")
    user_producer = setting_up(config=kafka_config, topic="twitter_users")

    while True:
        web3_users_info, tweets_list = get_web3_users_info(twitter_api, keywords, max_tweets_per_keyword=50)
        print(f"Collected information for {len(web3_users_info)} users.")

        for user_info in web3_users_info:
            key = user_info["id"]
            try:
                user_producer.send_message(key, user_info)
            except Exception as e:
                print(f"Error while sending user info to Kafka: {e}")
            user_producer.commit()

        for tweet in tweets_list:
            key = tweet["id"]
            try:
                tweet_producer.send_message(key, tweet)
            except Exception as e:
                print(f"Error while sending tweet to Kafka: {e}")
            tweet_producer.commit()

        time.sleep(300)  # Sleep for 5 minutes before fetching again


        




