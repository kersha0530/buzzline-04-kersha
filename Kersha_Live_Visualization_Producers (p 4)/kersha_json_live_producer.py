"""
kersha_json_live_producer.py

Stream JSON data to a file and a Kafka topic.

Example JSON message:
{
    "message": "I just shared a meme! It was amazing.",
    "author": "Charlie",
    "timestamp": "2025-01-29 14:35:20",
    "category": "humor",
    "sentiment": 0.87,
    "keyword_mentioned": "meme",
    "message_length": 42
}
"""

#####################################
# Import Modules
#####################################

import sys
import pathlib
import json
import os
import random
import time
from datetime import datetime
from dotenv import load_dotenv

# Dynamically add project root to sys.path
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

print(f"DEBUG: Added {PROJECT_ROOT} to sys.path")  # Debugging line

# Import utils
from utils.utils_logger import logger

# Import Kafka only if available
try:
    from kafka import KafkaProducer
    KAFKA_AVAILABLE = True
except ImportError:
    KAFKA_AVAILABLE = False

#####################################
# Load Environment Variables
#####################################

load_dotenv()

#####################################
# Define Constants and Keyword Categories
#####################################

KEYWORD_CATEGORIES = {
    "meme": "humor",
    "Python": "tech",
    "JavaScript": "tech",
    "recipe": "food",
    "travel": "travel",
    "movie": "entertainment",
    "game": "gaming",
}

#####################################
# Stub Sentiment Analysis Function
#####################################


def assess_sentiment(text: str) -> float:
    """Stub for sentiment analysis - returns a random value."""
    return round(random.uniform(0, 1), 2)


#####################################
# Getter Functions for Environment Variables
#####################################


def get_message_interval() -> int:
    """Fetch message interval from .env or use default."""
    return int(os.getenv("PROJECT_INTERVAL_SECONDS", 1))


def get_kafka_topic() -> str:
    """Fetch Kafka topic from .env or use default."""
    return os.getenv("BUZZ_TOPIC", "buzz_json")


def get_kafka_server() -> str:
    """Fetch Kafka server from .env or use default."""
    return os.getenv("KAFKA_SERVER", "localhost:9092")


#####################################
# Set up Paths
#####################################

DATA_FILE = pathlib.Path(__file__).parent.joinpath("buzz.json")

#####################################
# Define Message Generator
#####################################


def generate_messages():
    """
    Generate a stream of JSON messages with different authors.
    """
    ADJECTIVES = ["amazing", "funny", "boring", "exciting", "weird"]
    ACTIONS = ["found", "saw", "tried", "shared", "loved"]
    TOPICS = [
        "a movie",
        "a meme",
        "an app",
        "a trick",
        "a story",
        "Python",
        "JavaScript",
        "recipe",
        "travel",
        "game",
    ]
    AUTHORS = ["Alice", "Bob", "Charlie", "Eve", "Kersha"]  # Different authors

    while True:
        adjective = random.choice(ADJECTIVES)
        action = random.choice(ACTIONS)
        topic = random.choice(TOPICS)
        author = random.choice(AUTHORS)
        message_text = f"I just {action} {topic}! It was {adjective}."
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Find category based on keywords
        keyword_mentioned = next(
            (word for word in KEYWORD_CATEGORIES if word in topic), "other"
        )
        category = KEYWORD_CATEGORIES.get(keyword_mentioned, "other")

        # Assess sentiment
        sentiment = assess_sentiment(message_text)

        # Create JSON message
        json_message = {
            "message": message_text,
            "author": author,
            "timestamp": timestamp,
            "category": category,
            "sentiment": sentiment,
            "keyword_mentioned": keyword_mentioned,
            "message_length": len(message_text),
        }

        yield json_message


#####################################
# Main Function
#####################################


def main():
    """Start the producer and send messages to Kafka and a file."""
    logger.info("START producer...")
    interval_secs = get_message_interval()
    topic = get_kafka_topic()
    kafka_server = get_kafka_server()

    # Attempt to create Kafka producer
    producer = None
    if KAFKA_AVAILABLE:
        try:
            producer = KafkaProducer(
                bootstrap_servers=kafka_server,
                value_serializer=lambda x: json.dumps(x).encode("utf-8"),
            )
            logger.info(f"Kafka producer connected to {kafka_server}")
        except Exception as e:
            logger.error(f"Kafka connection failed: {e}")
            producer = None

    try:
        for message in generate_messages():
            logger.info(f"Generated message: {message}")

            # Write to local JSON file
            with open(DATA_FILE, "a") as f:
                f.write(json.dumps(message) + "\n")

            # Send to Kafka if available
            if producer:
                producer.send(topic, value=message)
                logger.info(f"Sent message to Kafka topic '{topic}': {message}")

            time.sleep(interval_secs)
    except KeyboardInterrupt:
        logger.warning("Producer interrupted by user.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        if producer:
            producer.close()
            logger.info("Kafka producer closed.")
        logger.info("Producer shutting down.")


#####################################
# Conditional Execution
#####################################

if __name__ == "__main__":
    main()

