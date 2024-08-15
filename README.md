# Real-Time-Sales-Dashboard
# Real-Time Eco Project: Streaming Data to HDFS & Live Dashboard with Django & Flask

<!-- TABLE OF CONTENTS -->
## Table of Contents
- [Introduction](#introduction)
- [System Architecture](#SystemArchitecture)
- [Tools Used](#ToolsUsed)
- [Getting Started](#GettingStarted)
- [Results](#Results)
<!-- END OF TABLE OF CONTENTS -->

<a name="introduction"></a>
## Introduction
This project is an end-to-end real-time eco project, focusing on data engineering and web application development. It involves real-time data ingestion, processing, and visualization using Hadoop, Spark, MySQL, and WebSockets, integrated with Flask frameworks. The goal is to stream live data to HDFS, process it with Spark, and visualize it on a live dashboard with Flask.

<a name="SystemArchitecture"></a>
## System Architecture
The system architecture consists of various stages:
1. **Data Streaming**: Data is streamed using Spark, partitioned by date and hour, and written to HDFS in Parquet format.
2. **Web Frameworks**: Django and Flask handle the front-end visualization, with Django managing real-time charts via WebSockets and MySQL.
3. **HDFS**: All processed data is stored in Hadoop's distributed file system for further analysis.
4. **MySQL Database**: Handles persistent storage of eco-related data for the web application.

<a name="ToolsUsed"></a>
## Tools Used

- **Hadoop (HDFS)**: Used to store data at scale, with real-time streaming and partitioning.
- **Apache Spark**: For real-time data streaming and transformation, writing to HDFS in Parquet format.
- **Django Framework**: Manages real-time eco data visualization using Channels and WebSockets.
- **Flask Framework**: Implements additional dashboard features, including pie and bar charts.
- **MySQL**: Stores eco project data and interfaces with Django for real-time data retrieval.
- **WebSockets**: Enables real-time communication between the server and the front-end, updating charts dynamically.
- **JavaScript & Chart.js**: Used to build dynamic, live-updating bar and pie charts on the web pages.

<a name="GettingStarted"></a>
## Getting Started
Follow these steps to set up the environment and start the project:

start the Zookeeper service:
``` bash
sudo systemctl start zookeeper
```
 start the Kafka service:
``` bash

sudo systemctl start kafka
```
### 1. Set Up Hadoop & Spark
Ensure Hadoop 3.3.6 and Spark are installed and configured. The streaming setup includes a Spark job that writes data to HDFS using the following code:
```python
orders_agg_write_stream_pre_hdfs = orders_df3.writeStream \
    .trigger(processingTime='10 seconds') \
    .format("parquet") \
    .option("path","/tmp/data/ecom_data/raw") \
    .option("checkpointLocation", "orders-agg-write-stream-pre-checkpoint") \
    .partitionBy("partition_date", "partition_hour") \
    .start()
