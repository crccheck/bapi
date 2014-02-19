import datetime
import os

from flask import abort, Flask, jsonify
import requests

import scrape


app = Flask(__name__)
cache = {}


@app.route('/<city_name>/')
def city(city_name):
    url = os.environ.get(city_name.upper())
    if not url:
        abort(404)
    cache_key = url
    now = datetime.datetime.now()
    output = cache.get(cache_key)
    if not output or now - output['now'] > datetime.timedelta(minutes=12):
        response = requests.get(
            url,
            headers={
                'User-Agent': 'bscrapeai/0.1',
            },
        )
        if response.status_code != 200:
            abort(response.status_code)
        data = scrape.find_data(response.text)
        output = {
            'city': city_name,
            'now': now,
            'result_length': len(data),
            'results': data,
        }
        cache[cache_key] = output
    return jsonify(output)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
