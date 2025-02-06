# Project: Buzzline-04-Kersha

# 📌 Project Overview
This repository contains real-time visualization scripts for consuming and producing messages. The scripts are structured into two primary folders:

## Kersha Live Visualisation Producers (p 4)/ – Producer scripts that generate and send messages.
## Kersha Live Visualisation Consumers (p 4)/ – Consumer scripts that read and visualize messages in real-time.
- Each folder contains three scripts:

### Basic JSON Producer/Consumer (No Kafka) – Writes and reads JSON messages from a file.
### CSV Producer/Consumer – Streams temperature sensor data from a CSV file.
### Project JSON Producer/Consumer – Sends and visualizes structured JSON messages.

🚀 Getting Started
1️. Install Dependencies
Ensure you have the required dependencies installed:

```bash```

pip install -r requirements.txt
2️. Running Producers
- The producer scripts generate and send messages.

#### Basic JSON Producer (No Kafka)

```bash```

python "Kersha Live Visualisation Producers (p 4)/kersha_basic_json(no kafka)live_producer.py"
CSV Producer

```bash```

python "Kersha Live Visualisation Producers (p 4)/kersha_csv_live_producer.py"
Project JSON Producer

```bash```

python "Kersha Live Visualisation Producers (p 4)/kersha_project_live_json_producer.py"
- Each script writes messages to a file or streams data to Kafka (if applicable).

3️. Running Consumers
Consumer scripts read messages and visualize them live.

#### Basic JSON Consumer (No Kafka, Reads from File)

```bash```

python "Kersha Live Visualisation Consumers (p 4)/kersha_basic_json(no kafka)live_consumer.py"
CSV Consumer (Reads from Kafka)

```bash```

python "Kersha Live Visualisation Consumers (p 4)/kersha_csv_live_consumer.py"
Project JSON Consumer (Reads from Kafka)

```bash```

python "Kersha Live Visualisation Consumers (p 4)/kersha_project_live_json_consumer.py"
- Each consumer opens a live Matplotlib plot that updates dynamically.

## Script Descriptions
🔹 Producer Scripts Description
- kersha_basic_json(no kafka)live_producer.py	Writes simple JSON messages to a file.
- kersha_csv_live_producer.py	Reads temperature sensor data from a CSV file and sends it to Kafka.
- kersha_project_live_json_producer.py	Streams structured JSON messages with metadata to Kafka.
🔹 Consumer Scripts Description
- kersha_basic_json(no kafka)live_consumer.py	Reads JSON messages from a file and visualizes message counts.
- kersha_csv_live_consumer.py	Reads temperature sensor data from Kafka and visualizes trends.
- kersha_project_live_json_consumer.py	Reads structured JSON messages from Kafka and visualizes data dynamically.

## Live Visualization
#### CSV Consumer: Displays a line chart of temperature over time.
#### JSON Consumer: Displays a bar chart of message counts by author.
- Each chart updates continuously as new messages arrive.


### Notes
Ensure your Kafka and Zookeeper are running before starting the producer and consumer.
Adjust the .env file for any custom configurations (e.g., Kafka broker address, topic name).


## About the Smart Smoker (CSV Example)

A food stall occurs when the internal temperature of food plateaus or 
stops rising during slow cooking, typically between 150°F and 170°F. 
This happens due to evaporative cooling as moisture escapes from the 
surface of the food. The plateau can last for hours, requiring 
adjustments like wrapping the food or raising the cooking temperature to 
overcome it. Cooking should continue until the food reaches the 
appropriate internal temperature for safe and proper doneness.

The producer simulates a smart food thermometer, sending a temperature 
reading every 15 seconds. The consumer monitors these messages and 
maintains a time window of the last 5 readings. 
If the temperature varies by less than 2 degrees, the consumer alerts 
the BBQ master that a stall has been detected. This time window helps 
capture recent trends while filtering out minor fluctuations.

## Later Work Sessions
When resuming work on this project:
1. Open the folder in VS Code. 
2. Start the Zookeeper service.
3. Start the Kafka service.
4. Activate your local project virtual environment (.env).

## Save Space
To save disk space, you can delete the .venv folder when not actively working on this project.
You can always recreate it, activate it, and reinstall the necessary packages later. 
Managing Python virtual environments is a valuable skill. 

## License
This project is licensed under the MIT License as an example project. 
You are encouraged to fork, copy, explore, and modify the code as you like. 
See the [LICENSE](LICENSE.txt) file for more.
