import json
import os

import redis


redis_url = os.getenv('REDISCLOUD_URL', 'redis://localhost:6379')
redis = redis.from_url(redis_url)


def memorize(func):
    name = func.__name__

    def wrapper(*args):
        key = name + '/' + '/'.join(args)

        if not redis.exists(key):
            redis.set(key, json.dumps(func(*args)))

        return json.loads(redis.get(key))

    return wrapper
