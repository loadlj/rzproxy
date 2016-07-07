#!/usr/bin/env python
import time
import logging

logger = logging.getLogger(__name__)


class Manager(object):
    def __init__(self, checker, queue, handler, interval=60):
        self._last_updatetime = queue.last_updatetime
        self._interval = interval
        self._is_handler_start = False
        self.handler = handler
        self.checker = checker

    def _schedule(self):
        # set up the crontab
        while True:
            now = int(time.time())
            if now - self._last_updatetime >= self._interval:
                logger.info("checking the proxy weight...")
                self.checker.check()
                self._last_updatetime = now
                self.handler.setup_cache()
                logger.info("the proxy list is checked over...")
            self._call_back()

    def _call_back(self):
        if self._is_handler_start:
            time.sleep(10)
        else:
            self._is_handler_start = True
            self.handler.setup_cache()
            self.handler.start()

    def run(self):
        self._schedule()
