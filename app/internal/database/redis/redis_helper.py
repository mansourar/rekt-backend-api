import logging
import os
from enum import Enum
from typing import Any

import redis
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class ModuleDB(int, Enum):
    LIVE_STATS = 0
    RESOURCE_CACHE = 1
    TOKENS = 2
    MATCH_SESSIONS = 3
    SIMULATED_MATCHMAKING_DATA = 4

    @classmethod
    def get_from_string(cls, string_name: str) -> "ModuleDB":
        match string_name:
            case "live_stats":
                return cls.LIVE_STATS
            case "ab_resource":
                return cls.RESOURCE_CACHE
            case "tokens":
                return cls.TOKENS
            case "match_sessions":
                return cls.MATCH_SESSIONS
            case "simulated_matchmaking_data":
                return cls.SIMULATED_MATCHMAKING_DATA

        raise ValueError(f"{string_name} does not map to a redis module")

    @classmethod
    def get_all(cls) -> list["ModuleDB"]:
        return [
            ModuleDB.LIVE_STATS,
            ModuleDB.RESOURCE_CACHE,
            ModuleDB.TOKENS,
            ModuleDB.MATCH_SESSIONS,
            ModuleDB.SIMULATED_MATCHMAKING_DATA,
        ]


class RedisConnector:
    def __init__(self, module_db: ModuleDB):
        load_dotenv()
        self.module_db = module_db
        self.key_prefix = f"{module_db.name}:"
        self.redis_pool = redis.ConnectionPool(
            host=os.getenv("REDIS_HOST"),
            port=int(os.getenv("REDIS_PORT")),
            max_connections=int(os.getenv("REDIS_POOL_SIZE")),
        )

    def get_conn(self):
        conn = redis.Redis(connection_pool=self.redis_pool)
        logger.info(
            f"Init Redis with host {os.getenv('REDIS_HOST')} and port {os.getenv('REDIS_PORT')}"
        )
        return conn

    def get_key(self, key):
        if isinstance(key, bytes):
            key = key.decode()
        key = key.replace(self.key_prefix, "")
        return (self.key_prefix + key).encode()

    def get(self, key):
        conn = self.get_conn()
        return conn.get(self.get_key(key))

    def set(self, key, value, ex=None):
        conn = self.get_conn()
        return conn.set(self.get_key(key), value, ex=ex)

    def delete(self, key):
        conn = self.get_conn()
        return conn.delete(self.get_key(key))

    def exists(self, key):
        conn = self.get_conn()
        return conn.exists(self.get_key(key))

    def keys(self, pattern="*"):
        conn = self.get_conn()
        keys = []
        cursor = 0
        while True:
            match = self.get_key(pattern)
            cursor, partial_keys = conn.scan(cursor, match=match)
            keys.extend(partial_keys)
            if cursor == 0:
                break
        return keys

    def expire(self, key, ttl):
        conn = self.get_conn()
        return conn.expire(self.get_key(key), ttl)

    def rpush(self, key, value):
        conn = self.get_conn()
        return conn.rpush(self.get_key(key), value)

    def ttl(self, key):
        conn = self.get_conn()
        return conn.ttl(self.get_key(key))

    def incr(self, key, incr_amount: int):
        conn = self.get_conn()
        return conn.incr(self.get_key(key), incr_amount)

    def flush_all(self):
        conn = self.get_conn()
        return conn.flushall()

    def publish(self, channel: str, message: Any):
        conn = self.get_conn()
        conn.publish(channel, message)
