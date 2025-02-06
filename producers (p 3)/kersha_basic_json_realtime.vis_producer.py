"""
json_realtime.vis_producer_kersha.py - Kafka producer for smoker temperature data.

Author: Kersha Broussard
Date: February 2025
"""

#####################################
# Import Modules
#####################################

import json
import os
import random
import time
import pathlib
from datetime import datetime

# Import Kafka
from kafka import KafkaProducer
from dotenv import load_dotenv

# Import logging
from utils.utils_logger import logger
from utils.utils_producer import create_kafka_producer, create_kafka_topic

#####################################
# Load Environment Variables
#####################################

load_dotenv()

#####################################
# Getter Functions for .env Variables
#####################################

def get_kafka_topic() -> str:
    """Fetch Kafka topic from environment or use default."""
    topic = os.getenv("KAFKA_TOPIC", "smoker_topic")  # Ensure it matches your consumer's topic
    logger.info(f"Kafka topic: {topic}")
    return topic

def get_message_interval() -> int:
    """Fetch message interval from environment or use default."""
    interval = int(os.getenv("SMOKER_INTERVAL_SECONDS", 1))
    logger.info(f"Message interval: {interval} seconds")
    return interval

#####################################
# Define Temperature Message Generator
#####################################

def generate_temperature_messages():
    """
    Generate real-time smoker temperature data.
    Example JSON message:
    {
        "timestamp": "2025-02-05T19:03:47.967875",
        "sensor_status": "inactive",
        "user_temp_setting": "160",
        "remote_control_status": "OFF",
        "temperature": 156.83,
        "status_message": "Sensor is inactive.",
        "temperature_status": "Warning: It's too hot!"
    }
    """
    while True:
        # Simulate sensor readings
        temperature = round(random.uniform(140, 180), 2)  # Simulated range
        sensor_status = random.choice(["active", "inactive"])
        user_temp_setting = random.choice(["150", "160", "170"])
        remote_control_status = random.choice(["ON", "OFF"])

        # Determine warnings
        if temperature > 170:
            temperature_status = "Warning: It's too hot!"
        elif temperature < 145:
            temperature_status = "Warning: It's too cold!"
        else:
            temperature_status = "Temperature is within range."

        # Construct message
        message = {
            "timestamp": datetime.utcnow().isoformat(),
            "sensor_status": sensor_status,
            "user_temp_setting": user_temp_setting,
            "remote_control_status": remote_control_status,
            "temperature": temperature,
            "status_message": f"Sensor is {sensor_status}.",
            "temperature_status": temperature_status
        }

        logger.debug(f"Generated message: {message}")
        yield message

#####################################
# Main Function
#####################################

def main():
    """Main function to send temperature data to Kafka."""
    logger.info("START JSON producer for smoker temperatures.")

    topic = get_kafka_topic()
    interval_secs = get_message_interval()

    # Create Kafka producer
    producer = create_kafka_producer(
        value_serializer=lambda x: json.dumps(x).encode("utf-8")
    )

    if not producer:
        logger.error("Failed to create Kafka producer. Exiting...")
        return

    # Ensure Kafka topic exists
    try:
        create_kafka_topic(topic)
        logger.info(f"Kafka topic '{topic}' is ready.")
    except Exception as e:
        logger.error(f"Failed to create or verify topic '{topic}': {e}")
        return

    # Send messages
    try:
        for message in generate_temperature_messages():
            producer.send(topic, value=message)
            logger.info(f"Sent message to topic '{topic}': {message}")
            time.sleep(interval_secs)
    except KeyboardInterrupt:
        logger.warning("Producer interrupted by user.")
    except Exception as e:
        logger.error(f"Error during message production: {e}")
    finally:
        producer.close()
        logger.info("Kafka producer closed.")

#####################################
# Conditional Execution
#####################################

if __name__ == "__main__":
    main()
