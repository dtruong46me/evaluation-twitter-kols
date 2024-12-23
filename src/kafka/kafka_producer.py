import os
import sys
from kafka import KafkaProducer
from hdfs import InsecureClient
import json
import logging
from typing import Dict, Any
import time


class TwitterKafkaProducer:
    def __init__(self, kafka_config: Dict[str, Any]):
        self.producer = KafkaProducer(
            bootstrap_servers=kafka_config['bootstrap_servers'],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

        self.tweet_topic = kafka_config["topics"]['tweet_topic']
        self.user_topic  = kafka_config["topics"]['user_topic']

    
    def send_tweet_to_stream(self, tweet_data: Dict[str, Any]) -> None:
        """
        Send tweet data to Kafka stream
        Args:
            tweet_data (Dict[str, Any]): Tweet data
        Returns:
            None
        """
        try:
            self.producer.send(topic=self.tweet_topic, value=tweet_data)
            print(f"Tweet sent to Kafka stream: {tweet_data['id']}")
            logging.info(f"Tweet sent to Kafka stream: {tweet_data['id']}")
        
        except Exception as e:
            logging.error(f"Error sending tweet to Kafka stream: {e}")

    
    def send_user_to_stream(self, user_data: Dict[str, Any]) -> None:
        """
        Send user data to Kafka stream
        Args:
            user_data (Dict[str, Any]): User data
        Returns:
            None
        """
        try:
            self.producer.send(topic=self.user_topic, value=user_data)
            print(f"User sent to Kafka stream: {user_data['id']}")
            logging.info(f"User sent to Kafka stream: {user_data['id']}")
        
        except Exception as e:
            logging.error(f"Error sending user to Kafka stream: {e}")

    
    def save_to_hdfs(self, hdfs_client: InsecureClient, hdfs_config: Dict[str, Any], data: Dict[str, Any]) -> None:
        """
        Save data to HDFS
        Args:
            hdfs_client (InsecureClient): HDFS client
            hdfs_config (Dict[str, Any]): HDFS configuration
            data (Dict[str, Any]): Data to save
        Returns:
            None
        """
        try:
            hdfs_client.write(hdfs_config['path'], data=json.dumps(data))
            logging.info(f"Data saved to HDFS: {data['id']}")
        
        except Exception as e:
            logging.error(f"Error saving data to HDFS: {e}")


def run():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    sys.path.insert(0, root)
    from src.utils import load_config

    kafka_config = load_config("kafka_config.yaml")
    print(kafka_config)
    producer = TwitterKafkaProducer(kafka_config=kafka_config)
    print("Kafka producer started")

    # Test tweet data
    test_data = [
        {
            "id": 1865963648138817884,
            "text": "RT @MookieNFT: Happy Sunday my dear friends! 💛\n\n\"𝐌𝐨𝐨𝐤𝐢𝐞’𝐬 𝐖𝐞𝐞𝐤𝐥𝐲 𝐑𝐞𝐜𝐚𝐩\" ✍️\n\nWeb3 &amp; Gaming News\n\nMy fam, this week has been full of exciting…",
            "author_id": 1484493749107695616,
            "created_at": "2024-12-09T03:36:16+00:00",
            "public_metrics": {
                "retweet_count": 38,
                "reply_count": 0,
                "like_count": 0,
                "quote_count": 0,
                "bookmark_count": 0,
                "impression_count": 0
            }
        },
        {
            "id": 1865963647287357808,
            "text": "RT @playweb3_io: One seamless API to evolve top Web2 hits into Web3 icons.\n\n20+ studios, 200+ games, 120M+ players…\n\nThe transformation beg…",
            "author_id": 1826143586376888323,
            "created_at": "2024-12-09T03:36:16+00:00",
            "public_metrics": {
                "retweet_count": 4547,
                "reply_count": 0,
                "like_count": 0,
                "quote_count": 0,
                "bookmark_count": 0,
                "impression_count": 0
            }
        },
        {
            "id": 1865963641784180962,
            "text": "RT @Web3manpro: Experience the future of Web3 with $STIX! Unleash the power of community and culture. Available now on Coinstore!\nJoin here…",
            "author_id": 1687683315623489536,
            "created_at": "2024-12-09T03:36:14+00:00",
            "public_metrics": {
                "retweet_count": 12,
                "reply_count": 0,
                "like_count": 0,
                "quote_count": 0,
                "bookmark_count": 0,
                "impression_count": 0
            }
        },
        {
            "id": 1865963636155625618,
            "text": "RT @playweb3_io: One seamless API to evolve top Web2 hits into Web3 icons.\n\n20+ studios, 200+ games, 120M+ players…\n\nThe transformation beg…",
            "author_id": 1853597396942688256,
            "created_at": "2024-12-09T03:36:13+00:00",
            "public_metrics": {
                "retweet_count": 4547,
                "reply_count": 0,
                "like_count": 0,
                "quote_count": 0,
                "bookmark_count": 0,
                "impression_count": 0
            }
        }
    ]

    # Send test data to Kafka stream
    for tweet in test_data:
        producer.send_tweet_to_stream(tweet_data=tweet)

        time.sleep(1)


if __name__=='__main__':
    run()