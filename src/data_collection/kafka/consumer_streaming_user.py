# CONSUME MESSAGE FROM KAFKA AND PROCESS THEN PUSH TO GCS AND BIGQUERY
from pyspark.sql import SparkSession
import pyspark.sql.functions as F

from pyspark.sql.types import (
    StructType, StructField, StringType, BooleanType, LongType
)
import os

PROJECT_ID = 'bigdata-of-truong'
CONSUME_TOPIC = 'users'

GCP_GCS_BUCKET = "business-analysis"
GCS_STORAGE_PATH = 'gs://' + GCP_GCS_BUCKET + '/realtime'
CHECKPOINT_PATH = 'gs://' + GCP_GCS_BUCKET + '/realtime/checkpoint/'
CHECKPOINT_PATH_BQ = 'gs://' + GCP_GCS_BUCKET + '/realtime/checkpoint_bq/'

KAFKA_CONFIG = {
    "bootstrap.servers":"pkc-n3603.us-central1.gcp.confluent.cloud:9092",
    "security.protocol":"SASL_SSL",
    "sasl.mechanisms":"PLAIN",
    "sasl.username":"YVDFCEBZP4JF5BHK",
    "sasl.password":"DQllCGVOzc4o7QPqfiJkAJyGZdxSD7xoHKeQeqBCvEqzcEGQPcNrmFht8tSA3PXI",
    "session.timeout.ms":45000,
    "client.id":"ccloud-python-client-8be9b834-4bcc-4831-bb62-23d035ac8e38"
}

def read_from_kafka(consume_topic: str):
    # Spark Streaming DataFrame, connect to Kafka topic served at host in bootrap.servers option
    df_stream = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_CONFIG["bootstrap.servers"]) \
        .option("subscribe", consume_topic) \
        .option("startingOffsets", "latest") \
        .option("checkpointLocation", CHECKPOINT_PATH) \
        .option("failOnDataLoss", "false") \
        .load()
    # .option("startingOffsets", "earliest") \
    return df_stream

def parse_user_from_kafka_message(kafka_df):
    """
    Take a Spark Streaming DataFrame and parse the value column based on the schema.
    Return a streaming DataFrame with columns in the specified schema.
    """
    assert kafka_df.isStreaming is True, "DataFrame doesn't receive streaming data"
    
    # Define the schema for the JSON data
    schema = StructType([
        StructField("id", StringType(), True),
        StructField("blue", BooleanType(), True),
        StructField("userName", StringType(), True),
        StructField("url", StringType(), True),
        StructField("displayName", StringType(), True),
        StructField("verified", BooleanType(), True),
        StructField("rawDescription", StringType(), True),
        StructField("followersCount", LongType(), True),
        StructField("friendsCount", LongType(), True),
        StructField("tweetCount", LongType(), True),
        StructField("listedCount", LongType(), True),
        StructField("created_at", StringType(), True),
        StructField("blueType", StringType(), True)
    ])
    
    # Parse the JSON from the "value" column
    tweets_df = kafka_df.selectExpr("CAST(value AS STRING)") \
        .select(F.from_json(F.col("value"), schema).alias("data")) \
        .select("data.*")
    
    return tweets_df

def create_file_write_stream(stream, storage_path, 
                             checkpoint_path='/checkpoint', 
                             trigger="5 seconds", 
                             output_mode="append", 
                             file_format="parquet",
                             partition_by="flight_date"):
    write_stream = (stream
                    .writeStream
                    .format(file_format)
                    .partitionBy(partition_by)
                    .option("path", storage_path)
                    .option("checkpointLocation", checkpoint_path)
                    .trigger(processingTime=trigger)
                    .outputMode(output_mode))

    return write_stream

def create_file_write_stream_bq(stream, 
                                checkpoint_path='/checkpoint', 
                                trigger="5 seconds", 
                                output_mode="append"):
    write_stream = (stream
                    .writeStream
                    .format("bigquery")
                    .option("table", f"{PROJECT_ID}.realtimes.flights")
                    .option("checkpointLocation", checkpoint_path)
                    .trigger(processingTime=trigger)
                    .outputMode(output_mode))

    return write_stream

if __name__=="__main__":
    spark = SparkSession.builder \
        .appName("Streaming from Kafka") \
        .config("spark.streaming.stopGracefullyOnShutdown", True) \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("DEBUG")
    spark.streams.resetTerminated()

    df_consume_stream = read_from_kafka(consume_topic=CONSUME_TOPIC)
    print(df_consume_stream.printSchema())

    # parse streaming data
    df_flight = parse_user_from_kafka_message(df_consume_stream)
    print(df_flight.printSchema())

    # Write to GCS
    write_stream_flights = create_file_write_stream(df_flight, GCS_STORAGE_PATH, checkpoint_path=CHECKPOINT_PATH, partition_by="flight_date")
    write_stream_flights_bq = create_file_write_stream_bq(df_flight,
                                                          checkpoint_path=CHECKPOINT_PATH_BQ)
 
    write_stream_flights.start()
    write_stream_flights_bq.start()
                                                        
    spark.streams.awaitAnyTermination()