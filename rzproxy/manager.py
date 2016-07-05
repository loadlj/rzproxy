#!/usr/bin/env python
import time
import logging
import multiprocessing

logger = logging.getLogger(__name__)


class Manager(multiprocessing.Process):
    def __init__(self, checker, queue, interval=30 * 60 * 60):
        multiprocessing.Process.__init__(self)
        self._last_updatetime = queue.last_updatetime
        self._interval = interval
        self.checker = checker

    def _schedule(self):
        # set up the crontab
        while True:
            now = time.time()
            if now - self._last_updatetime >= self._interval:
                self.checker.check()
                self._last_updatetime = now

    def run(self):
        self._schedule()
