from functools import wraps
import datetime
import os

from flask import abort, Flask, jsonify, request, current_app
import requests

import scrape


app = Flask(__name__)
cache = {}


# http://flask.pocoo.org/snippets/79/
def jsonp(func):
    """Wraps JSONified output for JSONP requests."""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            data = str(func(*args, **kwargs).data)
            content = str(callback) + '(' + data + ')'
            mimetype = 'application/javascript'
            return current_app.response_class(content, mimetype=mimetype)
        else:
            return func(*args, **kwargs)
    return decorated_function


@app.route('/<city_name>/')
@jsonp
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
