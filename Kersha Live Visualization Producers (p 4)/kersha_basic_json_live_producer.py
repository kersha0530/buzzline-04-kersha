import sys
import pathlib

# Dynamically add the project root to sys.path
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))  # Ensure project root is in Python path

print(f"DEBUG: Added {PROJECT_ROOT} to sys.path")  # Debugging line

# Now import utils
from utils.utils_logger import logger

import json
import time
import random


# Set up paths
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA_FOLDER = PROJECT_ROOT.joinpath("data")
DATA_FILE = DATA_FOLDER.joinpath("buzz.json")  # Ensure correct file

logger.info(f"Project root: {PROJECT_ROOT}")
logger.info(f"Data folder: {DATA_FOLDER}")
logger.info(f"Data file: {DATA_FILE}")

# List of sample messages & authors
MESSAGES = [
    "Data engineering is my passion.",
    "Distributed systems are fascinating.",
    "Have a great day!",
    "JSON makes life easier.",
    "Kafka is awesome.",
    "I love Python!",
    "Streaming data is fun.",
    "Buzz messages for everyone.",
]

AUTHORS = ["Alice", "Bob", "Charlie", "Diana", "Eve"]

def generate_message():
    """Generate a random JSON message."""
    message_data = {
        "message": random.choice(MESSAGES),
        "author": random.choice(AUTHORS),
    }
    return message_data

def write_message_to_file(message_data):
    """Append a new message to the buzz.json file."""
    try:
        # Read existing JSON content
        if DATA_FILE.exists():
            with open(DATA_FILE, "r") as file:
                try:
                    messages = json.load(file)  # Load existing list
                except json.JSONDecodeError:
                    logger.warning("Invalid JSON detected. Overwriting file.")
                    messages = []
        else:
            messages = []

        # Append new message
        messages.append(message_data)

        # Write updated list back to file
        with open(DATA_FILE, "w") as file:
            json.dump(messages, file, indent=4)

        logger.info(f"New message written: {message_data}")

    except Exception as e:
        logger.error(f"Error writing message to file: {e}")

def main():
    """Continuously generate and write messages to buzz.json."""
    logger.info("START producer.")
    try:
        while True:
            new_message = generate_message()
            write_message_to_file(new_message)
            time.sleep(2)  # Generate a new message every 2 seconds
    except KeyboardInterrupt:
        logger.info("Producer interrupted by user.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()



