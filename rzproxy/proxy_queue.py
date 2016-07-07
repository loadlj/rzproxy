#!/usr/bin/env python
import time
import redis


class ProxyQueue(object):
    def __init__(self, host='localhost', port=6379, db=0, password=None):
        self.queue = redis.StrictRedis(
                host=host, port=port, db=db, password=password)

    @property
    def best_proxy(self):
        max_value = 0
        max_key = ''
        for key in self.queue.keys():
            value = self.get(key)
            if value >= max_value:
                max_value = value
                max_key = key
        return max_key

    @property
    def setup_cache(self):
        cache = {}
        for key in self.queue.keys():
            cache[key] = self.get(key)
        return cache

    @property
    def last_updatetime(self):
        last_updatetime = 0
        for key in self.queue.keys():
            value, updatetime = self.queue.get(key).split(",")
            if updatetime >= last_updatetime:
                last_updatetime = updatetime
        return float(last_updatetime)

    def set(self, key, value, now=time.time()):
        # set value and updatetime
        result = str(value) + "," + str(now)
        self.queue.set(key, result)

    def _update(self, key, value):
        # not change the updatetime
        current_value, updatetime = self.queue.get(key).split(",")
        self.queue.set(key, str(value) + ',' + updatetime)

    def get(self, key):
        value, updatetime = self.queue.get(key).split(",")
        return float(value)

    def delete(self, key):
        self.queue.delete(key)

    def reduce_weight(self, key):
        current_value = self.get(key)
        self._update(key, current_value * 0.8)

    def add_weight(self, key):
        current_value = self.get(key)
        self._update(key, current_value / 0.8)
