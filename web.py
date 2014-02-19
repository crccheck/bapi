import datetime
import os

from flask import abort, Flask, jsonify
import requests

import scrape


app = Flask(__name__)


@app.route('/<city_name>/')
def city(city_name):
    url = os.environ.get(city_name.upper())
    if not url:
        abort(404)
    response = requests.get(
        url,
        headers={
            'User-Agent': 'bscrapeai/0.1',
        },
    )
    data = scrape.find_data(response.text)
    if response.status_code != 200:
        abort(response.status_code)
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
