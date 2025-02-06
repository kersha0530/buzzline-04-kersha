"""
smoker_chart.py - Real-time line chart for Smart BBQ Smoker temperature.

Author: Kersha Broussard
Date: February 2025
"""

import matplotlib.pyplot as plt
import pandas as pd
import time
import random  # Simulating real-time data (replace with CSV reader)

# List to store temperature readings
temperature_data = []

def update_smoker_chart():
    plt.ion()  # Enable interactive mode
    fig, ax = plt.subplots()

    while True:
        # Simulated temperature readings (Replace with actual CSV file reading)
        new_temp = random.uniform(145, 200)  # Example simulated temp
        temperature_data.append(new_temp)

        # Clear and update line chart
        ax.clear()
        ax.plot(temperature_data, marker='o', linestyle='-', color='red')
        ax.set_title("Smart BBQ Smoker - Real-Time Temperature Monitoring")
        ax.set_xlabel("Time (seconds)")
        ax.set_ylabel("Temperature (°F)")

        plt.pause(2)  # Adjust update frequency as needed

# Run the simulation
if __name__ == "__main__":
    update_smoker_chart()
