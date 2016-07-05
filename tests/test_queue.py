#!/usr/bin/env python
import time
import unittest

from rzproxy.proxy_queue import ProxyQueue


class TestQueue(unittest.TestCase):
    def setUp(self):
        self.queue = ProxyQueue()

    def test_get(self):
        self.queue.set("127.0.0.1", 123.00)
        self.assertEqual(self.queue.get("127.0.0.1"), 123.00)

    def test_reduce_weight(self):
        self.queue.set("127.0.0.1", 100.00)
        self.queue.reduce_weight("127.0.0.1")
        self.assertEqual(self.queue.get("127.0.0.1"), 80.00)

    def test_add_weight(self):
        self.queue.set("127.0.0.1", 100.00)
        self.queue.add_weight("127.0.0.1")
        self.assertEqual(self.queue.get("127.0.0.1"), 125.00)

    def test_set_updatetime(self):
        now = time.time()
        self.queue.set("127.0.0.1", 123.00, now)
        self.assertEqual(self.queue.last_updatetime, round(now, 2))

    def tearDown(self):
        self.queue.delete("127.0.0.1")
