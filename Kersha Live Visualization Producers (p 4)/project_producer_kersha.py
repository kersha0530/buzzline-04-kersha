
"""
project_producer_kersha.py

Generates sentiment data for Buzzline messages and writes to sentiment_live.json.
"""


import json
import random
import time
import pathlib
from datetime import datetime
from dotenv import load_dotenv
from utils.utils_logger import logger

# Load environment variables
load_dotenv()

# Define file path
PROJECT_ROOT = pathlib.Path(__file__).parent.parent
DATA_FILE = PROJECT_ROOT.joinpath("data", "sentiment_live.json")

MESSAGES = [
    "I love coding!",
    "Python makes data fun!",
    "Kafka is frustrating sometimes.",
    "Machine learning is exciting!",
    "I just saw a cool visualization!",
]

AUTHORS = ["Kersha", "Alice", "Bob", "Charlie", "Eve"]

def assess_sentiment(message):
    """Generate a sentiment score between -1 and 1."""
    return round(random.uniform(-1, 1), 2)

def generate_sentiment_messages():
    """Continuously generate new sentiment messages and update the JSON file."""
    while True:
        message = random.choice(MESSAGES)
        author = random.choice(AUTHORS)
        timestamp = datetime.utcnow().isoformat()
        sentiment_score = assess_sentiment(message)

        new_entry = {
            "timestamp": timestamp,
            "message": message,
            "author": author,
            "sentiment": sentiment_score
        }

        logger.info(f"Generated Sentiment Data: {new_entry}")

        # Read existing data
        existing_data = []
        if DATA_FILE.exists():
            try:
                with open(DATA_FILE, "r") as file:
                    existing_data = json.load(file)
            except json.JSONDecodeError:
                logger.error("JSON file corrupted. Starting fresh.")

        # Append new message and write to file
        existing_data.append(new_entry)
        with open(DATA_FILE, "w") as file:
            json.dump(existing_data, file, indent=4)

        time.sleep(2)  # Adjust interval as needed

if __name__ == "__main__":
    generate_sentiment_messages()
