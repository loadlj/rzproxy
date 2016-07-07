#!/usr/bin/env python
import click
import logging

from manager import Manager
from logger import set_logger
from proxy_queue import ProxyQueue
from check_proxy import ProxyCheck
from http_relay import HttpRelayHandler

logger = logging.getLogger(__name__)


def load_file(proxy_file):
    with open(proxy_file, 'rb') as r:
        for line in r.readlines():
            yield line.strip()


@click.command()
@click.option("--host", default="127.0.0.1", help="rzproxy host")
@click.option("--port", default=8399, help="rzproxy port", type=float)
@click.option("--file-name", help="proxy list file", required=True)
@click.option("--mysql-host", default="127.0.0.1", help="mysql host")
@click.option("--mysql-port", default=3306, help="mysql port", type=float)
@click.option("--db", default="rzproxy", help="mysql name")
@click.option("--user", default="root", help="mysql user")
@click.option("--password", help="mysql password")
@click.option("--interval", default=30 * 60, help="scheduler interval")
@click.option("--log-level", default="INFO",
              help="DEBUG, INFO, WARNING, ERROR, CRITICAL")
def main(host, port, file_name, mysql_host, mysql_port,
         db, user, password, interval, log_level):
    set_logger(getattr(logging, log_level))
    proxy_list = load_file(file_name)
    queue = ProxyQueue(mysql_host, mysql_port, db, user, password)
    checker = ProxyCheck(proxy_list, queue)
    relay_handler = HttpRelayHandler(queue)
    scheldurer = Manager(checker, queue, relay_handler, interval)
    scheldurer.run()

if __name__ == '__main__':
    main()
