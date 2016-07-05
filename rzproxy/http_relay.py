#!/usr/bin/env python
import socket
import logging

from gevent import pool
from gevent import select
from gevent.server import StreamServer
from gevent import monkey
monkey.patch_socket

BUF_SIZE = 4 * 1024

logger = logging.getLogger(__name__)


class HttpRelayHandler(object):
    # pool_count max is 100000
    # ensure the proxy weight is max
    def __init__(self, queue, proxy=("127.0.0.1", 8399), pool_count=100):
        self.proxy = proxy
        self.queue = queue
        self.pool = pool.Pool(pool_count)
        self.server = StreamServer(
                proxy, self._handle_connection, spawn=self.pool)

    def _handle_connection(self, local_sock, address):
        best_proxy = self.queue.best_proxy
        ip, port = best_proxy.split(":")
        logger.info("proxy is {}".format(best_proxy))
        try:
            remote_sock = self._create_remote_connection((ip, int(port)))
            while True:
                r, w, e = select.select(
                        [local_sock, remote_sock], [], [])
                if local_sock in r:
                    data = local_sock.recv(BUF_SIZE)
                    if remote_sock.send(data) <= 0:
                        break
                if remote_sock in r:
                    data = remote_sock.recv(BUF_SIZE)
                    if local_sock.send(data) <= 0:
                        break
            self.queue.add_weight(best_proxy)
            remote_sock.close()
        except Exception:
            # connection refused
            self.queue.reduce_weight(best_proxy)

    def _create_remote_connection(self, proxy):
        remote_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_sock.connect(proxy)
        return remote_sock

    def run(self):
        logger.info("Starting local server on {}.".format(self.proxy))
        self.server.serve_forever()
