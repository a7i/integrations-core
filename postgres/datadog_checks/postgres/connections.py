# (C) Datadog, Inc. 2023-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import datetime
import inspect
import threading
from typing import Callable, Dict
from collections import namedtuple

import psycopg2

ConnectionWithTTLAndLastAccess = namedtuple("ConnectionWithTTLAndLastAccess", "connection deadline last_access")

class MultiDatabaseConnectionPool(object):
    """
    Manages a connection pool across many logical databases with a maximum of 1 conn per
    database. Traditional connection pools manage a set of connections to a single database,
    however the usage patterns of the Agent application should aim to have minimal footprint
    and reuse a single connection as much as possible.

    Even when limited to a single connection per database, an instance with hundreds of
    databases still present a connection overhead risk. This class provides a mechanism
    to prune connections to a database which were not used in the time specified by their
    TTL.
    """

    class Stats(object):
        def __init__(self):
            self.connection_opened = 0
            self.connection_pruned = 0
            self.connection_closed = 0
            self.connection_closed_failed = 0

        def __repr__(self):
            return str(self.__dict__)

        def reset(self):
            self.__init__()

    def __init__(self, connect_fn):
        self._stats = self.Stats()
        self._mu = threading.Lock()
        self._conns = {}

        if hasattr(inspect, 'signature'):
            connect_sig = inspect.signature(connect_fn)
            if len(connect_sig.parameters) != 1:
                raise ValueError(
                    "Invalid signature for the connection function. "
                    "A single parameter for dbname is expected, got signature: {}".format(connect_sig)
                )
        self.connect_fn = connect_fn

    def get_connection(self, dbname, ttl_ms):
        self.prune_connections()
        with self._mu:
            conn = self._conns.pop(dbname, ConnectionWithTTLAndLastAccess(None, None, None))
            db = conn.connection
            if db is None or db.closed:
                self._stats.connection_opened += 1
                db = self.connect_fn(dbname)

            if db.status != psycopg2.extensions.STATUS_READY:
                # Some transaction went wrong and the connection is in an unhealthy state. Let's fix that
                db.rollback()

            deadline = datetime.datetime.now() + datetime.timedelta(milliseconds=ttl_ms)
            self._conns[dbname] = ConnectionWithTTLAndLastAccess(db, deadline, datetime.datetime.now())
            return db

    def prune_connections(self):
        """
        This function should be called periodically to prune all connections which have not been
        accessed since their TTL. This means that connections which are actually active on the
        server can still be closed with this function. For instance, if a connection is opened with
        ttl 1000ms, but the query it's running takes 5000ms, this function will still try to close
        the connection mid-query.
        """
        with self._mu:
            now = datetime.datetime.now()
            for dbname, conn in list(self._conns.items()):
                if conn.deadline < now:
                    self._stats.connection_pruned += 1
                    self._terminate_connection_unsafe(dbname)

    def close_all_connections(self):
        success = True
        with self._mu:
            while self._conns:
                dbname = next(iter(self._conns))
                if not self._terminate_connection_unsafe(dbname):
                    success = False
        return success

    def _terminate_connection_unsafe(self, dbname):
        db, _ = self._conns.pop(dbname, ConnectionWithTTLAndLastAccess(None, None, None))
        if db is not None:
            try:
                self._stats.connection_closed += 1
                db.close()
            except Exception:
                self._stats.connection_closed_failed += 1
                self._log.exception("failed to close DB connection for db=%s", dbname)
                return False
        return True

class MultiDatabaseConnectionPoolLimited(MultiDatabaseConnectionPool):
    """
    Managing multiple database connections, with a limit on concurrent connections.
    Evicts from the _conns pool with LRU rule, and also prunes connections after a specified TTL.
    """
    def __init__(self, connect_fn: Callable[[str], None], max_conn: int):
        super().__init__(connect_fn)
        self.max_conn = max_conn
        self.dbs_usage: Dict[str, bool] = {} # if connection should not be evicted, barring TTL expiration, set dbs_usage[db] = True here
        self._conns: Dict[str, ConnectionWithTTLAndLastAccess] = {}

    def _evict_lru(self) -> None:
        """
        Evict least recently used connection.
        Ensure lock is held before calling.
        """
        if len(self._conns) == 0:
            return

        lru = min(self._conns, key = lambda t: self._conns.get(t).last_access)
        if self.dbs_usage[lru]: # don't evict if query is running
            return

        self._conns.pop(lru)
        
    def get_connection(self, dbname: str, ttl_ms: int) -> psycopg2.extensions.connection:
        self.prune_connections()
        db_pool_len = 0
        with self._mu:
            db_pool_len = len(self._conns)

        if db_pool_len < self.max_conn:
            conn = super().get_connection(dbname, ttl_ms)
            self.dbs_usage[dbname] = True
            return conn

        with self._mu:
            while len(self._conns) > self.max_conn:
                self._evict_lru()

        conn = super().get_connection(dbname, ttl_ms)
        return conn