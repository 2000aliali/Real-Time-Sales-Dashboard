import streamlit as st
from kafka import KafkaProducer
from datetime import datetime
import random
from json import dumps
import time
from configparser import ConfigParser

# Loading Kafka configuration from a file
conf_file_name = "app.conf"
config_obj = ConfigParser()
config_obj.read(conf_file_name)

# Kafka Cluster/Server Details
kafka_host_name = config_obj.get('kafka', 'host')
kafka_port_no = config_obj.get('kafka', 'port_no')
kafka_topic_name = config_obj.get('kafka', 'input_topic_name')

KAFKA_TOPIC_NAME_CONS = kafka_topic_name
KAFKA_BOOTSTRAP_SERVERS_CONS = kafka_host_name + ':' + kafka_port_no

# Kafka producer setup
kafka_producer_obj = KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS_CONS,
                                   value_serializer=lambda x: dumps(x).encode('utf-8'))

# Streamlit interface
st.title("E-Commerce Order Producer")

# User inputs
product_name_list = ["Laptop", "Desktop Computer", "Mobile Phone", "Wrist Band", "Wrist Watch", "LAN Cable", "HDMI Cable",
                     "TV", "TV Stand", "Text Books", "External Hard Drive", "Pen Drive", "Online Course"]

order_card_type_list = ['Visa', 'Master', 'Maestro', 'American Express', 'Cirrus', 'PayPal']

country_name_city_name_list = ["Sydney,Australia", "Florida,United States", "New York City,United States", "Paris,France", 
                               "Colombo,Sri Lanka", "Dhaka,Bangladesh", "Islamabad,Pakistan", "Beijing,China", 
                               "Rome,Italy", "Berlin,Germany", "Ottawa,Canada", "London,United Kingdom", 
                               "Bangkok,Thailand", "Chennai,India", "Bangalore,India", 
                               "Mumbai,India", "Pune,India", "New Delhi,India", "Hyderabad,India", "Kolkata,India", 
                               "Singapore,Singapore"]

ecommerce_website_name_list = ["www.datamaking.com", "www.amazon.com", "www.flipkart.com", "www.snapdeal.com", "www.ebay.com"]

# Streamlit input widgets
product_name = st.selectbox("Select Product Name", product_name_list)
order_card_type = st.selectbox("Select Card Type", order_card_type_list)
order_amount = st.slider("Order Amount", min_value=5.5, max_value=555.5, step=1.0)
country_city = st.selectbox("Select Country and City", country_name_city_name_list)
ecommerce_website = st.selectbox("Select E-commerce Website", ecommerce_website_name_list)

# Button to send message to Kafka
if st.button("Send Order to Kafka"):
    # Prepare message
    country_name = country_city.split(",")[1]
    city_name = country_city.split(",")[0]
    
    message = {
        "order_id": random.randint(1, 1000),
        "order_product_name": product_name,
        "order_card_type": order_card_type,
        "order_amount": round(order_amount, 2),
        "order_datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "order_country_name": country_name,
        "order_city_name": city_name,
        "order_ecommerce_website_name": ecommerce_website
    }

    # Send message to Kafka
    kafka_producer_obj.send(KAFKA_TOPIC_NAME_CONS, message)
    st.success(f"Order {message['order_id']} sent to Kafka!")
