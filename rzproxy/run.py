#!/usr/bin/env python
import click
import logging

from manager import Manager
from logger import set_logger
from proxy_queue import ProxyQueue
from check_proxy import ProxyCheck
from http_relay import HttpRelayHandler

logger = logging.getLogger(__name__)
set_logger(logging.INFO)


def load_file(proxy_file):
    with open(proxy_file, 'rb') as r:
        for line in r.readlines():
            yield line.strip()


@click.command()
@click.option("--host", default="127.0.0.1", help="rzproxy host")
@click.option("--port", default=8399, help="rzproxy port", type=float)
@click.option("--file-name", help="proxy list file", required=True)
@click.option("--redis-host", default="127.0.0.1", help="redis host")
@click.option("--redis-port", default=6379, help="redis port", type=float)
@click.option("--db", default=0, help="redis database")
@click.option("--password", default=None, help="redis password")
@click.option("--interval", default=30 * 60 * 60, help="scheduler interval")
def main(host, port, file_name, redis_host, redis_port,
         db, password, interval):
    proxy_list = load_file(file_name)
    queue = ProxyQueue(redis_host, redis_port, db, password)
    checker = ProxyCheck(proxy_list, queue)
    scheldurer = Manager(checker, queue, interval)
    scheldurer.start()
    relay_handler = HttpRelayHandler(queue)
    relay_handler.run()

if __name__ == '__main__':
    main()
