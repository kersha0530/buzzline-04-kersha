"""
project_consumer_kersha.py
Reads sentiment trends from a JSON file and visualizes them in real-time.

🔹 No Kafka required! Reads from `project_live.json` instead.
🔹 Real-time sentiment trends based on messages received.
"""

import sys
import pathlib

# Dynamically add the project root to sys.path
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))  # Ensure project root is in Python path

print(f"DEBUG: Added {PROJECT_ROOT} to sys.path")  # Debugging line

# Now import utils
from utils.utils_logger import logger

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import json
import time
from collections import deque

# Define file path for sentiment storage
PROJECT_ROOT = pathlib.Path(__file__).parent.parent
DATA_FILE = PROJECT_ROOT.joinpath("data", "project_live.json")

# Store recent sentiment values
sentiment_values = deque(maxlen=50)  # Keep last 50 messages for trends
timestamps = deque(maxlen=50)

import os
from dotenv import load_dotenv
from utils.utils_consumer import create_kafka_consumer

# Initialize Matplotlib figure
fig, ax = plt.subplots()
ax.axhline(0, color="gray", linestyle="dashed", linewidth=1)  # Neutral sentiment reference line
ax.set_title("Kersha's Real-Time Sentiment Trend")
ax.set_xlabel("Time")
ax.set_ylabel("Sentiment Score")
plt.xticks(rotation=45)

def read_sentiment_data():
    """Read the latest sentiment value from `project_live.json`."""
    try:
        with open(DATA_FILE, "r") as file:
            lines = file.readlines()
            if lines:
                latest_entry = json.loads(lines[-1])  # Get the last message
                return latest_entry
    except (json.JSONDecodeError, FileNotFoundError):
        return None
    return None

def update_chart(frame):
    """Fetch new sentiment value from file and update the chart."""
    new_data = read_sentiment_data()

    if new_data:
        timestamp = new_data.get("timestamp", time.strftime("%H:%M:%S"))  # Default to current time
        sentiment = new_data.get("sentiment", 0)  # Default to neutral

        # Store data
        timestamps.append(timestamp)
        sentiment_values.append(sentiment)

        # Determine line color based on sentiment
        color = "green" if sentiment > 0.1 else "red" if sentiment < -0.1 else "yellow"

        # Clear previous graph and plot new line
        ax.clear()
        ax.axhline(0, color="gray", linestyle="dashed", linewidth=1) 
        ax.plot(timestamps, sentiment_values, marker="o", linestyle="-", color=color)

        # Update chart labels
        ax.set_title("Kersha's Real-Time Sentiment Trend")
        ax.set_xlabel("Time")
        ax.set_ylabel("Sentiment Score")
        plt.xticks(rotation=45)
        plt.tight_layout()

# Animation loop (updates every 2 seconds)
ani = animation.FuncAnimation(fig, update_chart, interval=2000)

# Run visualization
plt.show()
