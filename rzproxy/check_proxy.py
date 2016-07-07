#!/usr/bin/env python
import logging

import requests
from gevent import pool
from gevent import monkey
monkey.patch_all(thread=False, select=False)

TIME_OUT_SECOND = 5
HEADERS = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) " \
          "AppleWebKit/537.36 (KHTML, like Gecko) " \
          "Chrome/51.0.2704.103 Safari/537.36"
EXAMPLE_URL = [
    "http://www.baidu.com",
    "http://www.bing.com",
    "http://www.qq.com"
    ]

logger = logging.getLogger(__name__)


class ProxyCheck(object):
    def __init__(self, proxy_list, queue):
        self.proxy_list = proxy_list
        self.headers = {"User-Agent": HEADERS}
        self.queue = queue

    def _calculate_weight(self, proxy):
        # TODO check target url list
        weight = 0
        format_proxy = {"http": proxy}
        for target_url in EXAMPLE_URL:
            response_time = self._dump_reposne_time(format_proxy, target_url)
            weight += 1.0 / response_time if response_time > 0 else 0
        weight = weight / len(EXAMPLE_URL)
        self.queue.set(proxy, weight)

    def check(self):
        proxy_pool = pool.Pool(20)
        for proxy in self.proxy_list:
            proxy_pool.spawn(self._calculate_weight, proxy)
        proxy_pool.join()

    def _dump_reposne_time(self, proxy, url):
        try:
            r = requests.get(url=url, proxies=proxy, headers=self.headers,
                             timeout=TIME_OUT_SECOND)
            if r.status_code == 200:
                response_time = r.elapsed.total_seconds()
            else:
                response_time = -1
        except Exception:
            response_time = -1
        return response_time
