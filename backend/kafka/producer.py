import requests
from kafka import KafkaProducer


def fetch_raw(url, params):
    html = None
    print('Processing..{}'.format(url))
    try:
        r = requests.get(url, params=params)
        if r.status_code == 200:
            print('Responded 200')
            html = r.text
    except Exception as ex:
        print('Exception while accessing raw html')
        print(str(ex))
    finally:
        return html.strip()


def publish_message(producer_instance, topic_name, key, value):
    try:
        key_bytes = bytes(key, encoding='utf-8')
        value_bytes = bytes(value, encoding='utf-8')
        producer_instance.send(topic_name, key=key_bytes, value=value_bytes)
        producer_instance.flush()
        print('Message published successfully.')
    except Exception as ex:
        print('Exception in publishing message')
        print(str(ex))


def connect_kafka_producer():
    _producer = None
    try:
        _producer = KafkaProducer(bootstrap_servers=['localhost:9092'], api_version=(0, 10))
    except Exception as ex:
        print('Exception while connecting Kafka')
        print(str(ex))
    finally:
        return _producer


if __name__ == "__main__":
    topic_name = 'data'
    key = 'latest_data'
    value = fetch_raw('https://api.covidactnow.org/v2/states.json', {'apiKey': '0423b6788076433889e2c68b9985bb92'})
    kafka_producer = connect_kafka_producer()
    publish_message(kafka_producer, topic_name, key, value)
