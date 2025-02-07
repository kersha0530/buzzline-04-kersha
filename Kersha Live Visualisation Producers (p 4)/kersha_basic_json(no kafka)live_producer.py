"""
kersha_basic_json(no kafka)live_producer.py

"""
import sys
import pathlib

# Dynamically add the project root to sys.path
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

print(f"DEBUG: Added {PROJECT_ROOT} to sys.path")  # Debugging line

from utils.utils_logger import logger


import json
import os
import time
from collections import defaultdict
import matplotlib.pyplot as plt
from utils.utils_logger import logger

PROJECT_ROOT = pathlib.Path(__file__).parent.parent
DATA_FOLDER = PROJECT_ROOT.joinpath("data")
DATA_FILE = DATA_FOLDER.joinpath("buzz_live.json")

logger.info(f"Project root: {PROJECT_ROOT}")
logger.info(f"Data folder: {DATA_FOLDER}")
logger.info(f"Data file: {DATA_FILE}")

author_counts = defaultdict(int)

fig, ax = plt.subplots()
plt.ion()

def update_chart():
    ax.clear()
    authors_list = list(author_counts.keys())
    counts_list = list(author_counts.values())
    ax.bar(authors_list, counts_list, color="green")
    ax.set_xlabel("Authors")
    ax.set_ylabel("Message Counts")
    ax.set_title("Kersha's Basic Real-Time Author Message Counts")
    ax.set_xticklabels(authors_list, rotation=45, ha="right")
    plt.tight_layout()
    plt.draw()
    plt.pause(0.01)

def process_message(message: str) -> None:
    try:
        logger.debug(f"Raw message: {message}")
        message_dict = json.loads(message)
        logger.info(f"Processed JSON message: {message_dict}")
        if isinstance(message_dict, dict):
            author = message_dict.get("author", "unknown")
            logger.info(f"Message received from author: {author}")
            author_counts[author] += 1
            logger.info(f"Updated author counts: {dict(author_counts)}")
            update_chart()
        else:
            logger.error(f"Expected a dictionary but got: {type(message_dict)}")
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON message: {message}")
    except Exception as e:
        logger.error(f"Error processing message: {e}")

def main() -> None:
    logger.info("START consumer.")
    if not DATA_FILE.exists():
        logger.error(f"Data file {DATA_FILE} does not exist. Exiting.")
        sys.exit(1)
    try:
        with open(DATA_FILE, "r") as file:
            file.seek(0, os.SEEK_END)
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