#!/usr/bin/env python
import os

import redis

import portfolio
import server


redis_url = os.getenv('REDISCLOUD_URL', 'redis://localhost:6379')
redis = redis.from_url(redis_url)
categories = ('work', 'gettingmarried/stationery')

redis.flushdb()

for category in categories:
    for project in portfolio.projects(category):
        print project['src']
        parts = project['src'].strip('/').split('/')
        server.portfolio_data('/'.join(parts[:-1]), parts[-1])
