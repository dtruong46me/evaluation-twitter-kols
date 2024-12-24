from pyspark.sql.types import (
    StructType, StructField, StringType, DateType, IntegerType, TimestampType
)

BOOTSTRAP_SERVERS = ['localhost:9092', 'localhost:9093',]

PRODUCE_TOPIC_FLIGHTS = CONSUME_TOPIC_FLIGHTS = 'flight'

PRODUCE_TOPIC_TWEETS = 'tweets'
PRODUCE_TOPIC_USERS = 'users'
PROJECT_ID = 'bigdata-of-truong'
KAFKA_ADDRESS= "35.240.239.52"
KAFKA_BOOTSTRAP_SERVERS = f'{KAFKA_ADDRESS}:9092,{KAFKA_ADDRESS}:9093'
