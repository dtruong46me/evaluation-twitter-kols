from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

try:
    producer.send('twitter_tweets', b'Test message')
    print("Message sent successfully!")
except Exception as e:
    print(f"Error sending message: {e}")