from kafka import KafkaProducer
import json
from twitter_api import TwitterAPI
from utils import load_config
import time

class KafkaStreamer:
    def __init__(self, kafka_config: dict):
        self.producer = KafkaProducer(
            bootstrap_servers=kafka_config["bootstrap_servers"],
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )
        self.topic = kafka_config["topic"]

    def send_to_kafka(self, data):
        for record in data:
            try:
                self.producer.send(topic=self.topic, value=record)
                print(f"Sent to Kafka: {record}")
            except Exception as e:
                print(f"ERROR: {e}")

    def close_producer(self):
        self.producer.close()

if __name__ == "__main__":
    kafka_config = load_config("config/kafka_config.yml")
    twitter_api = TwitterAPI()
    kafka_streamer = KafkaStreamer(kafka_config)

    while True:
        tweets = twitter_api.search_tweets(query="python")
        kafka_streamer.send_to_kafka(tweets)
        time.sleep(60)