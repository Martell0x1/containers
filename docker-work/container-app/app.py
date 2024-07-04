from flask import Flask
import redis
import time

app = Flask(__name__)
cache = redis.Redis(host='redis',port=6379)

def get_hit_count():
      tries = 5
      while True:
            try:
                  return cache.incr('hits')
            except redis.exceptions.ConnectionError as exc:
                  if tries == 0:
                        return exc
                  tries -=1
                  time.sleep(0.5)
@app.route('/')
def hello_world():
    count = get_hit_count()
    return 'Hello , how are you doing , you"re now visiting me {}'.format(count)

if __name__ == '__main__':
        app.run(debug=False,host='0.0.0.0',port=5000)