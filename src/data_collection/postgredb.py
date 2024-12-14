import os
import sys
from typing import List, Any
import psycopg2
from psycopg2.extras import execute_batch

path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, path)

from utils import load_config

class PostgreDBM:
    def __init__(self, config: dict):
        self.config = config
        self.connection = self.connect_to_db()
    
    def connect_to_db(self) -> Any:
        """
        Connect to PostgreSQL Database
        """
        conn = psycopg2.connect(
            host=self.config['host'],
            port=self.config['port'],
            dbname=self.config['dbname'],
            user=self.config['user'],
            password=self.config['password']
        )
        return conn
    
    def store_users(self, users: List[dict]):
        """
        Store users into the Database
        """
        STORE_USERS_QUERY = """
        INSERT INTO users (id, username, followers, description, created_at)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING;
        """

        data = [
            (
                user['id'],
                user['username'],
                user['public_metrics']['followers_count'],
                user['description'],
                user['created_at']
            ) 
            for user in users
        ]

        with self.connection.cursor() as cursor:
            execute_batch(cursor=cursor, query=STORE_USERS_QUERY, argslist=data)
        
        self.connection.commit()


    def store_tweets(self, tweets: List[dict], user_id: str):
        """
        Store tweet data into the Database
        """
        STORE_TWEETS_QUERY = """
        INSERT INTO tweets (id, user_id, content, created_at, retweets, likes)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING;
        """
        data = [
            (
                tweet['id'],
                user_id,
                tweet['text'],
                tweet['created_at'],
                tweet['public_metrics']['retweet_count'],
                tweet['public_metrics']['like_count']
            )
            for tweet in tweets
        ]

        with self.connection.cursor() as cursor:
            execute_batch(cursor=cursor, query=STORE_TWEETS_QUERY, argslist=data)
        
        self.connection.commit()

    def create_schema(self):
        """
        Create the schema for the Database
        """
        CREATE_SCHEMA_QUERY = """
        CREATE TABLE IF NOT EXISTS users (
            id VARCHAR PRIMARY KEY,
            username VARCHAR,
            followers INT,
            description TEXT,
            created_at TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS tweets (
            id VARCHAR PRIMARY KEY,
            user_id VARCHAR,
            content TEXT,
            created_at TIMESTAMP,
            retweets INT,
            likes INT
        );
        """
        with self.connection.cursor() as cursor:
            cursor.execute(CREATE_SCHEMA_QUERY)
        
        self.connection.commit()

    def close_connection(self):
        """
        Close the connection to the Database
        """
        self.connection.close()


if __name__ == "__main__":
    config = load_config()

    dbm_config = config['postgresdb']

    dbm = PostgreDBM(config=dbm_config)
    dbm.create_schema()
    dbm.close_connection()