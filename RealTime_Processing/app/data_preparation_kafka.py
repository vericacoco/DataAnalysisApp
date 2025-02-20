import pandas as pd
from kafka import KafkaProducer
import json

# Читање на CSV податоци
df = pd.read_csv("stock_data_yahoo.csv")

# Конфигурирање на Kafka продучер
producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Испраќање на секој ред како порака во Kafka
for index, row in df.iterrows():
    producer.send('stock_data_topic', value=row.to_dict())
