# Project: Buzzline-04-Kersha

##  Overview
This project includes multiple **real-time producers and consumers** for visualizing live data. Producers generate data in **JSON** and **CSV** formats, while consumers process and display the data dynamically.


## Getting Started
### 1️.  Install Dependencies
- Ensure you have the required dependencies installed:

```bash```

pip install -r requirements.txt

#  Kersha Live Visualization - Producers & Consumers

##  Folder Structure
```
Kersha_Live_Visualization_Producers (p 4)/
│── kersha_basic_json_live_producer.py
│── kersha_csv_live_producer.py
│── kersha_json_live_producer.py
│── project_producer_case.py
│
Kersha_Live_Visualization_Consumers (p 4)/
│── kersha_basic_json_live_consumer.py
│── kersha_csv_live_consumer.py
│── kersha_json_live_consumer.py
│── project_consumer_kersha.py
```

---
## 🔹 Running the Producers & Consumers
Each **producer-consumer pair** should be executed separately to avoid conflicts.

### **1️. JSON Producer & Basic JSON Consumer**
 **Run the Producer:**
```sh
python "Kersha_Live_Visualization_Producers (p 4)/kersha_basic_json_live_producer.py"
```
 **Run the Consumer:**
```sh
python "Kersha_Live_Visualization_Consumers (p 4)/kersha_basic_json_live_consumer.py"
```

### **2️. JSON Producer & Advanced JSON Consumer**
 **Run the Producer:**
```sh
python "Kersha_Live_Visualization_Producers (p 4)/kersha_json_live_producer.py"
```
 **Run the Consumer:**
```sh
python "Kersha_Live_Visualization_Consumers (p 4)/kersha_json_live_consumer.py"
```

### **3️. CSV Producer & CSV Consumer**
✅ **Run the Producer:**
```sh
python "Kersha_Live_Visualization_Producers (p 4)/kersha_csv_live_producer.py"
```
✅ **Run the Consumer:**
```sh
python "Kersha_Live_Visualization_Consumers (p 4)/kersha_csv_live_consumer.py"
```

### **4️⃣ Project-Specific Producer & Consumer**
✅ **Run the Producer:**
```sh
python "Kersha_Live_Visualization_Producers (p 4)/project_producer_case.py"
```
✅ **Run the Consumer:**
```sh
python "Kersha_Live_Visualization_Consumers (p 4)/project_consumer_kersha.py"
```

---

1️⃣ **Activate Virtual Environment**
```sh
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

2️⃣ **Install Dependencies**
```sh
pip install -r requirements.txt
```

---
## **Expected Outputs**
- **JSON & CSV Consumers** generates **live visualizations** using Matplotlib.
- **Project Consumer** processes and **store insights** from the real-time messages.
- **Console logs** shows message ingestion and processing status.


#### - Each consumer script opens a live Matplotlib visualization.

📈 CSV Consumer: Displays a line chart of temperature over time.
📊 JSON Consumer: Displays a bar chart of message counts by author.
📉 Sentiment Consumer: Displays a dynamic line chart that reflects the data as:
🟢 Green → Positive sentiment
🔴 Red → Negative sentiment
🟡 Yellow → Neutral sentiment
#### Each chart updates continuously as new messages arrive.


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
