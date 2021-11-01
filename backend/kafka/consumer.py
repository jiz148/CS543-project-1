#consumer
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer('data', bootstrap_servers=['localhost:9092'],value_deserializer=lambda m: json.loads(m.decode('utf-8')))
#value_deserializer=lambda m: json.loads(m.decode('ascii'))

print(consumer)
for message in consumer:
    print("\n hello")
    print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,message.offset, message.key,message.value))
    


    
