import logging
import os
from uuid import uuid4
import requests

from confluent_kafka.serialization import  StringSerializer
from confluent_kafka import KafkaException

from .utils import delivery_report
from admin import Admin
from producer import ProducerClass
import json
#from settings import KAFKA_ADDRESS
import time

KAFKA_ADDRESS = "localhost:29092"

class JsonProducer(ProducerClass):
    def __init__(
        self,
        bootstrap_server,
        topic,
        compression_type=None,
        message_size=None,
        batch_size=None,
        waiting_time=None,
    ):
        super().__init__(
            bootstrap_server,
            topic,
            compression_type,
            message_size,
            batch_size,
            waiting_time,
        )
        self.string_serializer = StringSerializer("utf-8")

    def send_message(self, key=None, value=None):
        try:
            byte_value = (
                self.string_serializer(json.dumps(value)) if value else None
            )

            self.producer.produce(
                topic=self.topic,
                key=self.string_serializer(str(key)),
                value=byte_value,
                headers={"correlation_id": str(uuid4())},
                on_delivery=delivery_report,
            )
            logging.info("Message successfully produced by the producer")
        except KafkaException as e:
            kafka_error = e.args[0]
            if kafka_error.MSG_SIZE_TOO_LARGE:
                logging.error(
                    f"{e} , Current message size is {len(value) / (1024 * 1024)} MB"
                )
        except Exception as e:
            logging.error(f"Error while sending message: {e}")


def setting_up(config, topic):

    # Create Topic
    admin = Admin(config)
    admin.create_topic(topic, 3)  # second parameter is for number of partitions

    # Produce messages
    bootstrap_servers = config["bootstrap.servers"]
    producer = JsonProducer(
        bootstrap_servers,
        topic,
        compression_type="snappy",
        message_size=3 * 1024 * 1024,
        batch_size=10_00_00,  # in bytes, 1 MB
        waiting_time=10_000,  # in milliseconds, 10 seconds
    )
    return producer

if __name__ == "__main__":
    topic="twitter"
    producer = setting_up(KAFKA_ADDRESS, topic)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
    data_dir = os.path.join(root_dir, 'data')
