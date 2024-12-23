import unittest
from unittest.mock import patch, MagicMock
from src.twitter_api.kafka_streamer import KafkaStreamer

class TestKafkaStreamer(unittest.TestCase):
    @patch("src.kafka_streamer.KafkaProducer")
    def test_send_to_kafka(self, MockKafkaProducer):
        mock_producer = MockKafkaProducer.return_value
        kafka_config = {"bootstrap_servers": ["localhost:9092"], "topic": "test_topic"}
        kafka_streamer = KafkaStreamer(kafka_config)
        data = [{"id": 1, "text": "test tweet"}]

        kafka_streamer.send_to_kafka(data)
        mock_producer.send.assert_called_with(topic="test_topic", value=data[0])

if __name__ == "__main__":
    unittest.main()