import os
from redis import Redis
from flask import Flask, request, abort, jsonify
from utils import vcap


app = Flask(__name__)
port = os.getenv('PORT', '8080')
redis_creds = vcap.strip_redis_creds(vcap.creds('hsdp-redis-sentinel'))


@app.route('/hello')
def hello():
    return 'Hello World!'


@app.route('/')
def get_redis_key():
    r = Redis(**redis_creds)
    random_key = r.randomkey()
    if random_key:
        response = {random_key: r.get(random_key)}
    else:
        response = 'no data exists.'
    return jsonify(response)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))
else:
    application = app
