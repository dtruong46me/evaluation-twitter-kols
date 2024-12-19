from kafka import KafkaConsumer
import json
from utils import load_config

class KafkaConsumerApp:
    def __init__(self, kafka_config: dict):
        self.consumer = KafkaConsumer(
            kafka_config["topic"],
            bootstrap_servers=kafka_config["bootstrap_servers"],
            value_deserializer=lambda m: json.loads(m.decode("utf-8"))
        )

    def consume_messages(self):
        for message in self.consumer:
            print(f"Received message: {message.value}")

if __name__ == "__main__":
    kafka_config = load_config("config/kafka_config.yml")
    kafka_consumer_app = KafkaConsumerApp(kafka_config)
    kafka_consumer_app.consume_messages()