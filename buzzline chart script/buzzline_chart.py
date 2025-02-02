"""
buzzline_chart.py - Real-time bar chart for Buzzline message count by author.

Author: Kersha Broussard
Date: February 2025
"""

import matplotlib.pyplot as plt
from collections import defaultdict
import time
import random  # Simulating real-time data 

# Dictionary to store message count per author
author_message_counts = defaultdict(int)

def update_buzzline_chart():
    plt.ion()  # Enable interactive mode
    fig, ax = plt.subplots()

    while True:
        # Simulated incoming messages (Replace with Kafka consumer logic)
        new_author = random.choice(["Kersha", "Ian", "Carlos", "Kairo"])
        author_message_counts[new_author] += 1

        # Clear and update bar chart
        ax.clear()
        ax.bar(author_message_counts.keys(), author_message_counts.values(), color='blue')
        ax.set_title("Real-Time Buzz Messages Count by Author")
        ax.set_xlabel("Author")
        ax.set_ylabel("Message Count")

        plt.pause(.5) # Adjust update frequency as needed
# Run the simulation
if __name__ == "__main__":
    update_buzzline_chart()
