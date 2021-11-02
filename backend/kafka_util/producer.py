import requests
import threading

from kafka import KafkaProducer

API_DICT = {
    "country_level": {
        "url": "https://api.covidactnow.org/v2/states.timeseries.json",
        "params": {'apiKey': '0423b6788076433889e2c68b9985bb92'},
    },
    "state_level": {
        "url": "https://api.covidactnow.org/v2/state/{}.timeseries.json",
        "params": {'apiKey': '0423b6788076433889e2c68b9985bb92'},
    }
}
COUNTRY_TOPIC_NAME = 'country_level'
STATE_TOPIC_NAME = 'state_level'


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


def produce(state=None):
    kafka_producer = connect_kafka_producer()
    # country_level_value = None

    # produce state-level topic
    if state:
        state_url = API_DICT[STATE_TOPIC_NAME]["url"].format(state.upper())
        state_params = API_DICT[STATE_TOPIC_NAME]["params"]
        state_value = fetch_raw(state_url, state_params)
        print(state_value)
        publish_message(kafka_producer, STATE_TOPIC_NAME, 'latest_data', state_value)

    # produce country_level topic
    # country_url = API_DICT[COUNTRY_TOPIC_NAME]["url"]
    # country_params = API_DICT[COUNTRY_TOPIC_NAME]["params"]
    # country_value = fetch_raw(country_url, country_params)
    # publish_message(kafka_producer, COUNTRY_TOPIC_NAME, 'latest_data', country_value)


if __name__ == "__main__":
    thread_2 = threading.Thread(
        target=produce,
        args=('NJ',),
    )
    thread_2.start()
