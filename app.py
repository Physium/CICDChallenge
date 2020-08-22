from flask import Flask, render_template
from redis import Redis
import time
import os

app = Flask(__name__)
redis_host = os.environ.get('REDIS_SERVICE', 'localhost')
redis = Redis(host=redis_host, port=6379)


def get_hit_count():
    retries = 5
    while True:
        try:
            return redis.incr('hits')
        except Redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route('/feature')
def feature():
    return "Feature is up, testing 2nd branch. Change to test Jenkin PR Builder."


@app.route('/test')
def test():
    return "Flask Web Server is Up!"


@app.route('/')
def index():
    count = get_hit_count()
    pod_name = None

    if "POD_NAME" in os.environ:
        pod_name = os.environ['POD_NAME']

    return render_template("index.html", counter=count, pod=pod_name)


def print_hi(name):
    print(f'Hi, {name}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('Wei Jun')
    app.run(debug=True)