"""
csv_realtime.vis_consumer_kersha.py - Real-time bar chart for Buzzline message count by author.

Author: Kersha Broussard
Date: February 2025
"""
import sys
import pathlib

# Set project root correctly
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

print(f"DEBUG: Added {PROJECT_ROOT} to sys.path")  # Debugging line



from utils.utils_producer import create_kafka_producer  # For Producer
from utils.utils_consumer import create_kafka_consumer  # For Consumer


import os
import csv
import json
from dotenv import load_dotenv

import json
import time
import matplotlib.pyplot as plt
from collections import defaultdict
from dotenv import load_dotenv
from utils.utils_consumer import create_kafka_consumer
from utils.utils_logger import logger

# Load environment variables
load_dotenv()

def get_kafka_topic():
    return os.getenv("KAFKA_TOPIC", "smoker_topic")

def get_kafka_consumer_group_id():
    return os.getenv("KAFKA_CONSUMER_GROUP_ID", "default_group")

# Store temperature data
temperature_data = []

def process_message(message: str):
    """Process a single JSON message from Kafka and update the chart."""
    try:
        data = json.loads(message)
        timestamp = data.get("timestamp", "Unknown Time")
        temperature = float(data.get("temperature", 0))  # Ensure it's a number

        # Store the latest data for visualization
        timestamps.append(timestamp)
        temperature_values.append(temperature)

        if temperature is not None:
            temperature_data.append(temperature)
            print(f"DEBUG: Updated temperature data - {temperature_data}")  # Debug print

    except json.JSONDecodeError:
        print(f"ERROR: Invalid JSON message: {message}")
    except Exception as e:
        print(f"ERROR processing message: {e}")


    except json.JSONDecodeError:
        logger.error(f"Invalid JSON message: {message}")
    except Exception as e:
        logger.error(f"Error processing message: {e}")


import matplotlib.pyplot as plt
import time
from collections import deque

# Store recent temperature values
temperature_values = deque(maxlen=20)  # Keep the last 20 readings
timestamps = deque(maxlen=20)  # Store corresponding timestamps

def update_chart():
    """Continuously update the real-time temperature plot."""
    plt.ion()  # Enable interactive mode
    fig, ax = plt.subplots()

    while True:
        ax.clear()
        ax.plot(timestamps, temperature_values, marker='o', linestyle='-', color='blue')
        ax.set_title("Real-Time Smoker Temperature Data")
        ax.set_xlabel("Timestamp")
        ax.set_ylabel("Temperature (°F)")
        plt.xticks(rotation=45)
        plt.pause(1)  # Update every second



def main():
    """Main function to consume messages and update visualization."""
    topic = get_kafka_topic()
    group_id = get_kafka_consumer_group_id()
    consumer = create_kafka_consumer(topic, group_id)
    
    # Start visualization in a separate thread
    import threading
    chart_thread = threading.Thread(target=update_chart, daemon=True)
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
