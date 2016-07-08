#!/usr/bin/env python
import unittest
import gevent
import requests
from gevent import monkey
monkey.patch_socket()


class TestProxy(unittest.TestCase):
    def test_proxy(self):
        local_proxy = {"http": "http://127.0.0.1:8399"}

        def get():
            r = requests.get("http://www.baidu.com", proxies=local_proxy)
            self.assertEqual(r.status_code, 200)

        gevent_list = []
        for i in xrange(5):
            gevent_list.append(gevent.spawn(get))
        gevent.joinall(gevent_list)
