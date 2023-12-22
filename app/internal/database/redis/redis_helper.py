#  Copyright (c) Omeda Studios 2023.
import logging
from enum import Enum
from typing import Any

import redis
from dotenv import load_dotenv

from app.internal.helpers.components.environment import Environment

logger = logging.getLogger(__name__)
GLOBAL_ENV = Environment()


class ModuleDB(int, Enum):
    ASSETS_MANAGER = 0

    @classmethod
    def get_from_string(cls, string_name: str) -> "ModuleDB":
        match string_name:
            case "live_stats":
                return cls.ASSETS_MANAGER
        raise ValueError(f"{string_name} does not map to a redis module")

    @classmethod
    def get_all(cls) -> list["ModuleDB"]:
        return [
            ModuleDB.ASSETS_MANAGER
        ]


class RedisConnector:
    def __init__(self, module_db: ModuleDB):
        load_dotenv()
        self.module_db = module_db
        self.key_prefix = f"{module_db.name}:"
        self.redis_pool = redis.ConnectionPool(
            host=GLOBAL_ENV.REDIS_HOST,
            port=int(GLOBAL_ENV.REDIS_PORT),
            max_connections=int(GLOBAL_ENV.REDIS_POOL_SIZE),
        )
        self.conn = redis.Redis(connection_pool=self.redis_pool)

    def get_key(self, key):
        if isinstance(key, bytes):
            key = key.decode()
        key = key.replace(self.key_prefix, "")
        return (self.key_prefix + key).encode()

    def get(self, key):
        return self.conn.get(self.get_key(key))

    def set(self, key, value, ex=None):
        return self.conn.set(self.get_key(key), value, ex=ex)

    def delete(self, key):
        return self.conn.delete(self.get_key(key))

    def exists(self, key):
        return self.conn.exists(self.get_key(key))

    def keys(self, pattern="*"):
        conn = self.conn
        keys = []
        cursor = 0
        while True:
            match = self.get_key(pattern)
            cursor, partial_keys = self.conn.scan(cursor, match=match)
            keys.extend(partial_keys)
            if cursor == 0:
                break
        return keys

    def expire(self, key, ttl):
        return self.conn.expire(self.get_key(key), ttl)

    def rpush(self, key, value):
        return self.conn.rpush(self.get_key(key), value)

    def ttl(self, key):
        return self.conn.ttl(self.get_key(key))

    def incr(self, key, incr_amount: int):
        return self.conn.incr(self.get_key(key), incr_amount)

    def flush_all(self):
        return self.conn.flushall()

    def publish(self, channel: str, message: Any):
        self.conn.publish(channel, message)
