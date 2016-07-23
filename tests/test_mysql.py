#!/usr/bin/env python
import time
import unittest

from rzproxy.db.mysql_db import MysqlQueue


class TestQueue(unittest.TestCase):
    def setUp(self):
        self.queue = MysqlQueue(passwd="")

    def test_get(self):
        self.queue.set("127.0.0.1", 123.00)
        self.assertEqual(self.queue.get("127.0.0.1"), 123.00)

    def test_set_updatetime(self):
        now = time.time()
        self.queue.set("127.0.0.1", 123.00, now)
        self.assertEqual(self.queue.last_updatetime, round(now, 2))

    def tearDown(self):
        self.queue.remove("127.0.0.1")

if __name__ == "__main__":
    unittest.main()
