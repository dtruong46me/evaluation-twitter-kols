
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
        """
        Send data to Kafka topic
        Args:
            data (dict): List of tweet dictionaries
        """
        for record in data:
            try:
                self.producer.send(topic=self.topic, value=record)
                print(f"Sent to Kafka: {record}")
            
            except Exception as e:
                print(f"ERROR: {e}")
    
    def close_producer(self):
        self.producer.close()


if __name__=="__main__":
    # Load Kafka configuration
    kafka_config = load_config("kafka_config.yml")