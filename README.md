# Real-Time Sales Dashboard: Streaming Data to HDFS & Live Visualization with Flask

## Table of Contents
- [Introduction](#introduction)
- [System Architecture](#system-architecture)
- [Tools Used](#tools-used)
- [Getting Started](#getting-started)
- [Results](#results)

## Introduction
The Real-Time Sales Dashboard project is an end-to-end data engineering and web application that focuses on real-time data ingestion, processing, and visualization. The project streams data from Kafka to HDFS, processes it using Spark, and visualizes it on a live dashboard built with Flask. Real-time updates are powered by WebSockets, ensuring that the dashboard displays the most current data at all times.

## System Architecture
The system architecture consists of the following components:
![Screenshot](https://github.com/2000aliali/Real-Time-Sales-Dashboard/blob/main/Images/Capture%20d'%C3%A9cran%202024-08-16%20052425.png)
1. **Data Streaming**: Real-time data is streamed from Kafka to Spark, where it is processed and partitioned by date and hour, then written to HDFS in Parquet format.
2. **Web Framework**: Flask serves the front-end web application, displaying real-time sales data using dynamically updated charts. The data is retrieved from MySQL and sent to the front-end via WebSockets for real-time updates.
3. **HDFS**: The processed data is stored in Hadoop's distributed file system, ensuring scalable and reliable data storage.
4. **MySQL Database**: Acts as the storage layer for the processed sales data, which is then queried by the Flask app to generate real-time visualizations.

## Tools Used
- **Hadoop (HDFS)**: For distributed storage and real-time streaming.
- **Apache Spark**: For real-time data processing and transformation before writing to HDFS.
- **Kafka & Zookeeper**: Kafka streams real-time data, while Zookeeper manages distributed synchronization for Kafka.
- **Flask**: A lightweight web framework used to build the live dashboard that visualizes the data with charts.
- **MySQL**: Stores the processed data, which the Flask app queries to generate visualizations.
- **WebSockets**: Enables real-time updates on the web dashboard by pushing new data from the server to the front-end.
- **JavaScript & Chart.js**: Powers the dynamic charts that visualize the data on the web page.

## Getting Started

Follow the steps below to set up and run the project:

1. **Clone the Project**
   ```bash
   git clone https://github.com/2000aliali/Real-Time-Sales-Dashboard.git
   cd Real-Time-Sales-Dashboard


2. **insatll the liberrary** 
pip install -r requirements.txt

3. **start the Zookeeper service**
``` bash
sudo systemctl start zookeeper
```
3.  **start the Kafka service**
``` bash

sudo systemctl start kafka
```
4. **Run the spark job**
``` bash
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0,mysql:mysql-connector-java:5.1.49 --files /home/ali-el-azzaouy/Documents/real_time_eco_project/realtime_data_processing/app.conf realtime_data_processing.py
```
5.  **Run our dasboard**
``` bash
python app2.py 
```

## Results
Go through this video to see the exact steps and the results: [Watch the video](https://drive.google.com/file/d/1pjGh_pcp2nZVQHVbcpJFVDbyEoU1Y2NU/view?usp=sharing)

