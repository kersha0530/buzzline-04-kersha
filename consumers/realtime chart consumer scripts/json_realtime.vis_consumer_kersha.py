"""
json_realtime.vis_consumer_kersha.py - Real-time bar chart for Buzzline message count by author.

Author: Kersha Broussard
Date: February 2025
"""
import sys
import pathlib

# Manually set the project root directory
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

print(f"DEBUG: Added {PROJECT_ROOT} to sys.path")  # Debugging line

from utils.utils_consumer import create_kafka_consumer  # Import AFTER sys.path update
from utils.utils_logger import logger

import os
import json
import time
import random
import matplotlib.pyplot as plt
from collections import defaultdict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_kafka_topic() -> str:
    """Fetch Kafka topic from environment or use default."""
    topic = os.getenv("BUZZ_TOPIC", "unknown_topic")
    logger.info(f"Kafka topic: {topic}")
    return topic


def get_kafka_consumer_group_id() -> str:
    """Fetch Kafka consumer group ID from environment or use default."""
    group_id = os.getenv("BUZZ_CONSUMER_GROUP_ID", "default_group")
    logger.info(f"Kafka consumer group id: {group_id}")
    return group_id

# Dictionary to store message count per author
author_message_counts = defaultdict(int)

def process_message(message: str) -> None:
    """Process a single JSON message from Kafka."""
    try:
        message_dict = json.loads(message)
        author = message_dict.get("author", "unknown")
        author_message_counts[author] += 1
        logger.info(f"Updated author counts: {dict(author_message_counts)}")
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON message: {message}")
    except Exception as e:
        logger.error(f"Error processing message: {e}")

def update_buzzline_chart():
    """Continuously update the real-time bar chart as Kafka messages are processed."""
    plt.ion()
    fig, ax = plt.subplots()

    while True:
        ax.clear()
        ax.bar(author_message_counts.keys(), author_message_counts.values(), color='blue')
        ax.set_title("Real-Time Buzz Messages Count by Author")
        ax.set_xlabel("Author")
        ax.set_ylabel("Message Count")
        plt.pause(0.5)  # Adjust if needed

    plt.show(block=True)  # Ensures the window stays open


def main():
    """Main function to consume Kafka messages and update visualization."""
    topic = get_kafka_topic()
    group_id = get_kafka_consumer_group_id()
    consumer = create_kafka_consumer(topic, group_id)
    
    # Start visualization in a separate thread
    import threading
    chart_thread = threading.Thread(target=update_buzzline_chart, daemon=True)
    chart_thread.start()

    logger.info(f"Consuming messages from Kafka topic '{topic}'...")
    try:
        for message in consumer:
            process_message(message.value)
    except KeyboardInterrupt:
        logger.warning("Consumer interrupted by user.")
    except Exception as e:
        logger.error(f"Error while consuming messages: {e}")
    finally:
        consumer.close()
        logger.info("Kafka consumer closed.")

if __name__ == "__main__":
    main()