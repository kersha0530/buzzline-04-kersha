"""
kersha_csv_live_producer.py

Stream numeric temperature data to a Kafka topic.
"""

#####################################
# Import Modules
#####################################
import sys
import pathlib

# Dynamically add the project root to sys.path
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))  # Ensure project root is in Python path

print(f"DEBUG: Added {PROJECT_ROOT} to sys.path")  # Debugging line

# Now import utils
from utils.utils_logger import logger

import os
import time
import csv
import json
from datetime import datetime
from dotenv import load_dotenv
from utils.utils_producer import (
    verify_services,
    create_kafka_producer,
    create_kafka_topic,
)
from utils.utils_logger import logger

#####################################
# Load Environment Variables
#####################################

load_dotenv()

def get_kafka_topic() -> str:
    """Fetch Kafka topic from environment or use default."""
    topic = os.getenv("SMOKER_TOPIC", "smoker_csv")  # Default topic
    logger.info(f"Kafka topic: {topic}")
    return topic

def get_message_interval() -> int:
    """Fetch message interval from environment or use default."""
    interval = int(os.getenv("SMOKER_INTERVAL_SECONDS", 5))  # Default 5 seconds
    logger.info(f"Message interval: {interval} seconds")
    return interval

#####################################
# Set up Paths
#####################################

PROJECT_ROOT = pathlib.Path(__file__).parent.parent
DATA_FOLDER = PROJECT_ROOT.joinpath("data")
DATA_FILE = DATA_FOLDER.joinpath("smoker_temps.csv")
logger.info(f"Data file: {DATA_FILE}")

#####################################
# Message Generator
#####################################

def generate_messages(file_path: pathlib.Path):
    """Read from a CSV file and yield records one by one."""
    try:
        with open(file_path, "r") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                if "temperature" not in row:
                    logger.error(f"Missing 'temperature' column in row: {row}")
                    continue
                current_timestamp = datetime.utcnow().isoformat()
                message = {
                    "timestamp": current_timestamp,
                    "temperature": float(row["temperature"]),
                }
                yield message
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}. Exiting.")
        sys.exit(1)

#####################################
# Define main function
#####################################

def main():
    """Main function to send messages to Kafka."""
    logger.info("START producer.")
    verify_services()
    topic = get_kafka_topic()
    interval_secs = get_message_interval()
    
    if not DATA_FILE.exists():
        logger.error(f"Data file not found: {DATA_FILE}. Exiting.")
        sys.exit(1)
    
    producer = create_kafka_producer(
        value_serializer=lambda x: json.dumps(x).encode("utf-8")
    )
    if not producer:
        logger.error("Failed to create Kafka producer. Exiting...")
        sys.exit(3)
    
    create_kafka_topic(topic)  # Ensures topic is created before sending messages
    
    try:
        for csv_message in generate_messages(DATA_FILE):
            producer.send(topic, value=csv_message)
            logger.info(f"Sent message to topic '{topic}': {csv_message}")
            time.sleep(interval_secs)  # Wait before sending next message
    except KeyboardInterrupt:
        logger.warning("Producer interrupted by user.")
    finally:
        producer.close()
        logger.info("Kafka producer closed.")

if __name__ == "__main__":
    main()

