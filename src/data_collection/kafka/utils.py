import os

from dotenv import load_dotenv

import logging

def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

def load_env():
    """Loads environment variables from a .env file"""

    dotenv_path = os.path.join(os.path.dirname(__file__), "../.env")
    load_dotenv(dotenv_path)

def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed for record {msg.key()}: {err}")
    else:
        print(
            f"Record {msg.key()} successfully produced to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}"
        )

def read_config():
  # reads the client configuration from client.properties
  # and returns it as a key-value map
  root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
  client_path = os.path.join(root, "src", "data_collection", "kafka", "client.properties")
  config = {}

  with open(client_path) as fh:
    for line in fh:
      line = line.strip()
      if len(line) != 0 and line[0] != "#":
        parameter, value = line.strip().split('=', 1)
        config[parameter] = value.strip()
  return config