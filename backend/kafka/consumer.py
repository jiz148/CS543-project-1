#consumer
from kafka import KafkaConsumer

consumer = KafkaConsumer('data', bootstrap_servers=['localhost:9092'],value_deserializer=lambda m: json.loads(m.decode('ascii')))

for message in consumer:
    print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,message.offset, message.key,message.value))


    
