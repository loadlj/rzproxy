#!/usr/bin/env python
import time
import logging
import sqlite3

logger = logging.getLogger(__name__)


class SqliteQueue(object):
    def __init__(self):
        self._conn = sqlite3.connect("rzproxy.db")
        self._execute('''CREATE TABLE IF NOT EXISTS proxy_pool (
             `proxy` text PRIMARY KEY,
             `weight` real,
             `updatetime` real
             )''')

    @property
    def best_proxy(self):
        result_cur = self._execute(
            "SELECT proxy FROM proxy_pool ORDER BY weight DESC LIMIT 1")
        return result_cur.fetchone()[0]

    @property
    def last_updatetime(self):
        result_cur = self._execute("SELECT updatetime FROM proxy_pool\
                                   ORDER BY updatetime DESC LIMIT 1")
        result = result_cur.fetchone()
        if result:
            return result[0]
        else:
            # start checking proxy list
            return 0

    @property
    def setup_cache(self):
        cache = {}
        result_list = self._execute("select proxy, weight from proxy_pool")
        for result in result_list.fetchall():
            cache[result[0]] = result[1]
        return cache

    def get(self, key):
        result_cur = self._execute(
            "SELECT weight FROM proxy_pool WHERE proxy='{}'".format(key))
        return result_cur.fetchone()[0]

    def set(self, key, value, now=time.time()):
        self._execute("REPLACE INTO proxy_pool VALUES('{0}', {1}, {2})"
                      .format(key, value, now))

    def commit(self):
        self._conn.commit()

    def remove(self, key):
        self._execute("DELETE FROM proxy_pool WHERE proxy='{}'".format(key))

    def _execute(self, sql_query, values=[]):
        dbcur = self._dbcur()
        dbcur.execute(sql_query, values)
        return dbcur

    def _dbcur(self):
        return self._conn.cursor()
