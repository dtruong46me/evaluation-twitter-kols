from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql.functions import col

# Initialize Spark session
PROJECT_ID = 'bigdata-of-truong'
GCP_BUCKET = 'business-analysis'
GCS_STORAGE_PATH = 'gs://' + GCP_BUCKET + '/batch/tweet'

MONGO_URI = "mongodb+srv://truong:uMPXa75rVh5HDuFs@cluster0.ah4ovlj.mongodb.net/"

COMMON_COLUMNS = [
    "_id",
    "author",
    "created",
    'timestamp',
    "url",
    "views",
    "likes",
    "replyCount",
    "retweetCount",
    "text"
]

# MongoDB connection details
mongo_db = "kols_db"
mongo_collection = "tweets"

# Read data from MongoDB
def read_from_mongo(spark, db: str, collection: str) -> DataFrame:
    df = spark.read \
        .format("mongodb") \
        .option("database", db) \
        .option("collection", collection) \
        .load()
    return df

def parse_schema_from_mongo(df: DataFrame):
    existing_columns = [col for col in COMMON_COLUMNS if col in df.columns]
    df = df.select(*existing_columns)
    return df

# Write data to GCS
def write_to_gcs(df: DataFrame, path: str):
    df.write \
        .format("parquet") \
        .mode("overwrite") \
        .partitionBy("author") \
        .save(path)

def write_to_bq(df: DataFrame, table_name: str):
    df.write \
        .format("bigquery") \
        .option("table", table_name) \
        .mode("overwrite") \
        .save()

# Main function
if __name__ == "__main__":
    spark = SparkSession.builder \
        .appName("MongoDBToGCS") \
        .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:10.4.0") \
        .config("spark.mongodb.input.partitioner", "SamplePartitioner") \
        .config("spark.mongodb.read.connection.uri", MONGO_URI) \
        .getOrCreate()
    
    df = read_from_mongo(spark, mongo_db, mongo_collection)
    df = parse_schema_from_mongo(df)

    write_to_gcs(df, GCS_STORAGE_PATH)
    write_to_bq(df, f"{PROJECT_ID}.twitter_kols.twitter_tweets")
    
    spark.stop()