import base64

from flask import Flask, send_file, jsonify
from flask_cors import CORS


application = Flask(__name__)
# CORS
CORS(application)


@application.route('/', methods=['POST'])
def query():
    with open("data/us_map.png", "rb") as image_file:
        image = base64.b64encode(image_file.read()).decode("utf-8")
    return jsonify({'status': True, 'image': image})


@application.route('/us', methods=['GET'])
def query_us():
    with open("data/us_map.png", "rb") as image_file:
        image = base64.b64encode(image_file.read()).decode("utf-8")
    return jsonify({'status': True, 'image': image})


if __name__ == '__main__':
    application.run()