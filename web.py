from flask import Flask
app = Flask(__name__)


@app.route('/<city_name>/')
def city(city_name):
    return 'Hello {}!'.format(city_name)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
