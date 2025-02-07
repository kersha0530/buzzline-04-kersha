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
import os
import time
import matplotlib.pyplot as plt
from collections import defaultdict


# Set up paths
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA_FOLDER = PROJECT_ROOT.joinpath("data")
DATA_FILE = DATA_FOLDER.joinpath("buzz.json")  # Ensure correct file

logger.info(f"Project root: {PROJECT_ROOT}")
logger.info(f"Data folder: {DATA_FOLDER}")
logger.info(f"Data file: {DATA_FILE}")

# Data structure for tracking message counts
author_counts = defaultdict(int)

# Set up Matplotlib for real-time visualization
fig, ax = plt.subplots()
plt.ion()  # Enable interactive mode

def update_chart():
    """Update the live chart with the latest author message counts."""
    ax.clear()
    authors = list(author_counts.keys())
    counts = list(author_counts.values())

    ax.bar(authors, counts, color="green")
    ax.set_xlabel("Authors")
    ax.set_ylabel("Message Counts")
    ax.set_title("Kersha's Real-Time Author Message Counts")
    ax.set_xticklabels(authors, rotation=45, ha="right")

    plt.tight_layout()
    plt.draw()
    plt.pause(0.01)  # ✅ Ensures real-time updates

def process_message(message: str) -> None:
    """Process an incoming JSON message and update visualization."""
    try:
        message_dict = json.loads(message)

        if isinstance(message_dict, dict) and "author" in message_dict:
            author = message_dict["author"]
            author_counts[author] += 1
            logger.info(f"New message from {author}: {message_dict['message']}")
            update_chart()
        else:
            logger.error(f"Invalid message format: {message_dict}")

    except json.JSONDecodeError:
        logger.error(f"Failed to decode JSON message: {message}")

def main() -> None:
    """Main consumer function that reads and visualizes messages in real-time."""
    logger.info("START consumer.")

    if not DATA_FILE.exists():
        logger.error(f"Data file {DATA_FILE} does not exist. Exiting.")
        sys.exit(1)

    try:
        # Read existing messages
        with open(DATA_FILE, "r") as file:
            try:
                messages = json.load(file)  # ✅ Load JSON list at start
                for msg in messages:
                    process_message(json.dumps(msg))  # Convert back to string
            except json.JSONDecodeError:
                logger.error("Failed to load JSON from file. Check formatting.")

        # Open file in read mode and watch for new lines
        with open(DATA_FILE, "r") as file:
            file.seek(0, os.SEEK_END)  # Move cursor to end for new messages
            print("Consumer is ready and waiting for new JSON messages...")

            while True:
                line = file.readline()
                if line.strip():
                    process_message(line)
                else:
                    logger.debug("No new messages. Waiting...")
                    time.sleep(0.5)

    except KeyboardInterrupt:
        logger.info("Consumer interrupted by user.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        plt.ioff()
        plt.show()
        logger.info("Consumer closed.")

if __name__ == "__main__":
    main()




