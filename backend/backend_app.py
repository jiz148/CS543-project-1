import base64
from io import BytesIO

from flask import Flask, jsonify, request
from flask_cors import CORS

from backend.kafka_util import consumer
from backend.common import visualizer


application = Flask(__name__)
# CORS
CORS(application)


@application.route('/', methods=['POST'])
def query():
    with open("data/us_map.png", "rb") as image_file:
        image = base64.b64encode(image_file.read()).decode("utf-8")
    # get params
    plot_type = request.form.get('plot_type')
    date_from = request.form.get('date_from')
    date_to = request.form.get('date_to')
    state = request.form.get('state')

    print(plot_type, date_from, date_to, state)
    img = _produce_to_plot(plot_type, date_from, date_to, state)
    # Create a buffer to hold the bytes
    buf = BytesIO()
    # Save the image as jpeg to the buffer
    img.save(buf, 'png')
    # Rewind the buffer's file pointer
    buf.seek(0)
    # Read the bytes from the buffer
    image_bytes = buf.read()
    # Close the buffer
    buf.close()
    image = base64.b64encode(image_bytes).decode("utf-8")
    return jsonify({'status': True, 'image': image})


@application.route('/us', methods=['GET'])
def query_us():
    with open("data/us_map.png", "rb") as image_file:
        image = base64.b64encode(image_file.read()).decode("utf-8")
    return jsonify({'status': True, 'image': image})


def _produce_to_plot(plot_type, date_from, date_to, state):
    # result = {}
    # thread_1 = threading.Thread(
    #     target=consumer.consumer,
    #     args=(plot_type, data_from, data_to, state, result),
    # )
    # thread_2 = threading.Thread(
    #     target=producer.produce,
    #     args=(state,),
    # )
    # thread_1.start()
    # thread_2.start()
    # producer.produce(state)

    # data = consumer.consumer(plot_type, data_from, data_to, state, result)
    # print(result['result'])
    data = consumer.consumer(plot_type, date_from, date_to, state)
    img = visualizer.visualize(plot_type, data, state, date_from, date_to)
    # print(consumer.consumer('hist', '2021-05-01', '2021-9-05', 'nj'))

    return img


if __name__ == '__main__':
    application.run()