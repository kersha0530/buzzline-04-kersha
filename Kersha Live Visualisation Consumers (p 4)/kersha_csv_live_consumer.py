"""
kersha_csv_live_consumer.py

Consume JSON messages from a Kafka topic and visualize temperature readings in real-time.

Example Kafka message format:
{"timestamp": "2025-01-11T18:15:00Z", "temperature": 225.0}
"""

#####################################
# Import Modules
#####################################

import os
import json  # handle JSON parsing
from collections import deque
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from utils.utils_consumer import create_kafka_consumer
from utils.utils_logger import logger

#####################################
# Load Environment Variables
#####################################

load_dotenv()

def get_kafka_topic() -> str:
    """Fetch Kafka topic from environment or use default."""
    topic = os.getenv("SMOKER_TOPIC", "unknown_topic")
    logger.info(f"Kafka topic: {topic}")
    return topic

def get_kafka_consumer_group_id() -> str:
    """Fetch Kafka consumer group id from environment or use default."""
    group_id: str = os.getenv("SMOKER_CONSUMER_GROUP_ID", "default_group")
    logger.info(f"Kafka consumer group id: {group_id}")
    return group_id

def get_rolling_window_size() -> int:
    """Fetch rolling window size from environment or use default."""
    window_size = int(os.getenv("SMOKER_ROLLING_WINDOW_SIZE", 5))
    logger.info(f"Rolling window size: {window_size}")
    return window_size

#####################################
# Set up data structures (empty lists)
#####################################

timestamps = []  # To store timestamps for the x-axis
temperatures = []  # To store temperature readings for the y-axis

#####################################
# Set up live visuals
#####################################

fig, ax = plt.subplots()
plt.ion()

#####################################
# Define an update chart function for live plotting
#####################################

def update_chart():
    """Update temperature vs. time chart."""
    ax.clear()
    ax.plot(timestamps, temperatures, label="Temperature", color="blue")
    ax.set_xlabel("Time")
    ax.set_ylabel("Temperature (\u00b0F)")
    ax.set_title("Kersha's Smart Smoker: Temperature vs. Time")
    ax.legend()
    fig.autofmt_xdate()
    plt.tight_layout()
    plt.draw()
    plt.pause(0.01)

#####################################
# Function to process a single message
#####################################

def process_message(message: str) -> None:
    """Process a JSON-transferred CSV message."""
    try:
        data = json.loads(message)
        temperature = data.get("temperature")
        timestamp = data.get("timestamp")
        logger.info(f"Processed JSON message: {data}")

        if temperature is None or timestamp is None:
            logger.error(f"Invalid message format: {message}")
            return

        timestamps.append(timestamp)
        temperatures.append(temperature)
        update_chart()

    except json.JSONDecodeError as e:
        logger.error(f"JSON decoding error for message '{message}': {e}")
    except Exception as e:
        logger.error(f"Error processing message '{message}': {e}")

#####################################
# Define main function for this module
#####################################

def main() -> None:
    """Main entry point for the consumer."""
    logger.info("START consumer.")
    timestamps.clear()
    temperatures.clear()
    topic = get_kafka_topic()
    group_id = get_kafka_consumer_group_id()
    logger.info(f"Consumer: Topic '{topic}' and group '{group_id}'...")
    consumer = create_kafka_consumer(topic, group_id)
    logger.info(f"Polling messages from topic '{topic}'...")
    try:
        for message in consumer:
            message_str = message.value
            process_message(message_str)
    except KeyboardInterrupt:
        logger.warning("Consumer interrupted by user.")
    except Exception as e:
        logger.error(f"Error while consuming messages: {e}")
    finally:
        consumer.close()
        logger.info(f"Kafka consumer for topic '{topic}' closed.")

#####################################
# Conditional Execution
#####################################

if __name__ == "__main__":
    main()
    plt.ioff()
    plt.show()
