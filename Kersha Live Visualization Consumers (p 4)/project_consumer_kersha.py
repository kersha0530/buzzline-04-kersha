############################################################################
"""

project_consumer_kersha.py
Visualizes real-time sentiment trends from Buzzline messages.
Reads sentiment values from `sentiment_live.json`.

This visualization tracks sentiment trends in real-time based on messages received. The line chart will display the sentiment score of messages over time, helping identify shifts in positivity or negativity.

📈 Live-Updating Line Graph: The x-axis shows timestamps of when messages arrive, and the y-axis represents sentiment scores (ranging from -1 to 1).
🟢 Positive Sentiments (Above 0): Indicate happy or encouraging messages.
🔴 Negative Sentiments (Below 0): Indicate frustration or dissatisfaction.
🟡 Neutral Sentiments (Near 0): Messages that are neither positive nor negative.
🚀 Trends Over Time: If messages get more positive, the line trends upward. If negativity rises, it trends downward.

"""


import matplotlib.pyplot as plt
import matplotlib.animation as animation
import json
import time
import pathlib
from collections import deque

# Define file path for sentiment storage
PROJECT_ROOT = pathlib.Path(__file__).parent.parent
DATA_FILE = PROJECT_ROOT.joinpath("data", "sentiment_live.json")

# Store recent sentiment values
sentiment_values = deque(maxlen=50)  # Keep last 50 messages for trends
timestamps = deque(maxlen=50)

# Initialize Matplotlib figure
fig, ax = plt.subplots()
ax.axhline(0, color="gray", linestyle="dashed", linewidth=1)  # Neutral sentiment reference line
ax.set_title("🚀 Kersha's Real-Time Sentiment Trend for Buzzline")
ax.set_xlabel("Time")
ax.set_ylabel("Sentiment Score")
plt.xticks(rotation=45)

def read_sentiment_data():
    """Read sentiment values from `sentiment_live.json`."""
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
            if isinstance(data, list) and len(data) > 0:
                return data[-1]  # Return the latest sentiment message
    except (json.JSONDecodeError, FileNotFoundError):
        return None
    return None

def update_chart(frame):
    """Fetch new sentiment value from file, update trend line, and change color dynamically."""
    new_data = read_sentiment_data()

    if new_data:
        timestamp = time.strftime("%H:%M:%S")  # Use current time
        sentiment = new_data.get("sentiment", 0)  # Get sentiment score

        # Store data
        timestamps.append(timestamp)
        sentiment_values.append(sentiment)

        # Determine line color based on sentiment
        if sentiment > 0.1:
            color = "green"  # 🟢 Positive
        elif sentiment < -0.1:
            color = "red"  # 🔴 Negative
        else:
            color = "yellow"  # 🟡 Neutral

        # Clear previous graph and plot new line
        ax.clear()
        ax.axhline(0, color="gray", linestyle="dashed", linewidth=1) 
        ax.plot(timestamps, sentiment_values, marker="o", linestyle="-", color=color)

        # Update chart labels
        ax.set_title("🚀 Kersha's Real-Time Sentiment Trend for Buzzline")
        ax.set_xlabel("Time")
        ax.set_ylabel("Sentiment Score")
        plt.xticks(rotation=45)
        plt.tight_layout()

# Animation loop (updates every 2 seconds)
ani = animation.FuncAnimation(fig, update_chart, interval=2000)

# Run visualization
plt.show()


