#!/usr/bin/env python
import click
import logging

from manager import Manager
from logger import set_logger
from check_proxy import ProxyCheck
from db.sqlite_db import SqliteQueue
from db.mysql_db import MysqlQueue
from http_relay import HttpRelayHandler

logger = logging.getLogger(__name__)


def load_file(proxy_file):
    with open(proxy_file, 'rb') as r:
        for line in r.readlines():
            yield line.strip()


@click.command()
@click.option("--host", default="127.0.0.1", help="rzproxy host")
@click.option("--db-type", default="sqlite", help="mysql, sqlite")
@click.option("--port", default=8399, help="rzproxy port", type=int)
@click.option("--file-name", help="proxy list file", required=True)
@click.option("--mysql-host", default="127.0.0.1", help="mysql host")
@click.option("--mysql-port", default=3306, help="mysql port", type=float)
@click.option("--db", default="rzproxy", help="mysql name")
@click.option("--user", default="root", help="mysql user")
@click.option("--password", help="mysql password")
@click.option("--target-url", default=None,
              help="the target url you will crawl")
@click.option("--interval", default=30 * 60,
              help="scheduler interval", type=float)
@click.option("--log-level", default="INFO",
              help="DEBUG, INFO, WARNING, ERROR, CRITICAL")
def main(host, db_type, port, file_name, mysql_host, mysql_port,
         db, user, password, target_url, interval, log_level):
    set_logger(getattr(logging, log_level))
    proxy_list = load_file(file_name)
    if db_type == "sqlite":
        queue = SqliteQueue()
    else:
        queue = MysqlQueue(mysql_host, mysql_port, db, user, password)
    checker = ProxyCheck(proxy_list, queue, target_url)
    relay_handler = HttpRelayHandler(queue, (host, port))
    scheldurer = Manager(checker, queue, relay_handler, interval)
    scheldurer.run()

if __name__ == '__main__':
    main()
