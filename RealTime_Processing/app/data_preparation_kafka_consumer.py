from kafka import KafkaConsumer
import json

# Конфигурирање на Kafka консумер
consumer = KafkaConsumer(
    'stock_data_topic',
    bootstrap_servers='localhost:9092',
    group_id='stock_data_group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# Читање и печатење на порки
for message in consumer:
    print(message.value)
