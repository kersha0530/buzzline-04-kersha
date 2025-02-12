"""
kersha_csv_live_consumer.py

Consume JSON messages from a Kafka topic and visualize temperature readings in real-time.

Example Kafka message format:
{"timestamp": "2025-01-11T18:15:00Z", "temperature": 225.0}
"""

#####################################
# Import Modules
#####################################

import sys
import pathlib

# Add project root directory to sys.path
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Add utils directory explicitly
UTILS_PATH = str(PROJECT_ROOT.joinpath("utils"))
if UTILS_PATH not in sys.path:
    sys.path.append(UTILS_PATH)

print(f"DEBUG: Added {PROJECT_ROOT} and {UTILS_PATH} to sys.path")  # Debugging line

# Now import utils
from utils.utils_logger import logger
from utils.utils_consumer import create_kafka_consumer


import os
import matplotlib

# Set DISPLAY environment variable for GUI in WSL
os.environ["DISPLAY"] = "192.168.80.1:0"  

# Use TkAgg for Matplotlib GUI rendering
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
import json
from collections import deque
from dotenv import load_dotenv
from utils.utils_consumer import create_kafka_consumer


# Dynamically add the project root to sys.path
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

print(f"DEBUG: Added {PROJECT_ROOT} to sys.path")  # Debugging line

#####################################
# Load Environment Variables
#####################################

load_dotenv()

def get_kafka_topic():
    """Fetch Kafka topic from environment or use default."""
    topic = os.getenv("SMOKER_TOPIC", "smoker_csv")
    logger.info(f"Kafka topic: {topic}")
    return topic

def get_kafka_consumer_group_id():
    """Fetch Kafka consumer group id from environment or use default."""
    group_id = os.getenv("SMOKER_CONSUMER_GROUP_ID", "smoker_group")
    logger.info(f"Kafka consumer group id: {group_id}")
    return group_id

def get_rolling_window_size():
    """Fetch rolling window size from environment or use default."""
    window_size = int(os.getenv("SMOKER_ROLLING_WINDOW_SIZE", 10))  # Increased default to 10
    logger.info(f"Rolling window size: {window_size}")
    return window_size

#####################################
# Set up Data Structures
#####################################

timestamps = deque(maxlen=get_rolling_window_size())  # Store recent timestamps
temperatures = deque(maxlen=get_rolling_window_size())  # Store recent temperatures

#####################################
# Set up Live Visualization
#####################################

plt.ion()  # Enable interactive mode
fig, ax = plt.subplots()

import matplotlib.pyplot as plt

plt.ion()  # Enable interactive mode
fig, ax = plt.subplots()

# Force the plot to open
plt.show(block=False)  

def update_chart():
    """Update the live chart with temperature readings."""
    print(f"DEBUG: Updating chart with {len(timestamps)} data points")  # Debugging line

    if len(timestamps) == 0 or len(temperatures) == 0:
        print("DEBUG: No data received yet.")
        return  # Prevent errors if no data is available

    ax.clear()
    ax.plot(timestamps, temperatures, label="Temperature", color="blue", marker="o")

    ax.set_xlabel("Time")
    ax.set_ylabel("Temperature (°F)")
    ax.set_title("Kersha's Smart Smoker: Temperature vs. Time")
    ax.legend()
    fig.autofmt_xdate()
    plt.tight_layout()
    plt.draw()
    plt.pause(0.1)  # Allow time for the chart to update
    print("DEBUG: Chart updated!")  # Debugging output



#####################################
# Function to Process Messages
#####################################

def process_message(message: str):
    """Process a JSON-transferred Kafka message."""
    try:
        data = json.loads(message)
        temperature = data.get("temperature")
        timestamp = data.get("timestamp")

        if temperature is None or timestamp is None:
            logger.error(f"Invalid message format: {message}")
            return

        timestamps.append(timestamp)
        temperatures.append(temperature)
        logger.info(f"Processed message: {data}")
        update_chart()

    except json.JSONDecodeError as e:
        logger.error(f"JSON decoding error: {e}")
    except Exception as e:
        logger.error(f"Error processing message: {e}")

#####################################
# Define Main Consumer Function
#####################################

def main():
    """Main entry point for the Kafka consumer."""
    logger.info("START consumer.")
    topic = get_kafka_topic()
    group_id = get_kafka_consumer_group_id()

    logger.info(f"Consumer subscribing to topic '{topic}' with group '{group_id}'...")
    consumer = create_kafka_consumer(topic, group_id)

    try:
        for message in consumer:
            print(f"DEBUG: Received {message.value}")  # Ensure messages are coming in
            process_message(message.value)
    except KeyboardInterrupt:
        logger.warning("Consumer interrupted by user.")
    except Exception as e:
        logger.error(f"Error while consuming messages: {e}")
    finally:
        consumer.close()
        logger.info(f"Kafka consumer for topic '{topic}' closed.")

#####################################
# Run Consumer if Executed as Script
#####################################

if __name__ == "__main__":
    main()
    plt.ioff()  # Disable interactive mode when script ends
    print("DEBUG: Calling plt.show() to display the chart.")  # Debugging output
    plt.show()  # Ensure the chart opens and stays open







