import unittest
from unittest.mock import patch, MagicMock
from src.data_collection.kafka_consumer import KafkaConsumerApp

class TestKafkaConsumerApp(unittest.TestCase):
    @patch("src.kafka_consumer.KafkaConsumer")
    def test_consume_messages(self, MockKafkaConsumer):
        mock_consumer = MockKafkaConsumer.return_value
        mock_consumer.__iter__.return_value = [MagicMock(value={"id": 1, "text": "test tweet"})]
        kafka_config = {"bootstrap_servers": ["localhost:9092"], "topic": "test_topic"}
        kafka_consumer_app = KafkaConsumerApp(kafka_config)

        with patch("builtins.print") as mock_print:
            kafka_consumer_app.consume_messages()
            mock_print.assert_called_with("Received message: {'id': 1, 'text': 'test tweet'}")

if __name__ == "__main__":
    unittest.main()