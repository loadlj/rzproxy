#!/usr/bin/env python
import time
import unittest

from rzproxy.db.sqlite_db import SqliteQueue


class TestQueue(unittest.TestCase):
    def test_get(self):
        queue = SqliteQueue()
        queue.set("127.0.0.1", 1.122)
        self.assertEqual(queue.get("127.0.0.1"), 1.122)
        queue.remove("127.0.0.1")

    def test_set_updatetime(self):
        queue = SqliteQueue()
        now = time.time()
        queue.set("127.0.0.1", 123.00, now)
        self.assertEqual(queue.last_updatetime, round(now, 2))
        queue.remove("127.0.0.1")

    def test_setup_cache(self):
        queue = SqliteQueue()
        queue.set("127.0.0.1", 123.12)
        cache = queue.setup_cache
        self.assertEqual(cache["127.0.0.1"], 123.12)
        queue.remove("127.0.0.1")


if __name__ == "__main__":
    unittest.main()
