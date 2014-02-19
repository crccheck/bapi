import datetime

from flask import Flask, jsonify

import scrape


app = Flask(__name__)


@app.route('/<city_name>/')
def city(city_name):
    with open('test_data.txt', 'r') as f:
        data = scrape.find_data(f.read())
    output = {
        'city': city_name,
        'now': datetime.datetime.now(),
        'result_length': len(data),
        'results': data,
    }
    return jsonify(output)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
