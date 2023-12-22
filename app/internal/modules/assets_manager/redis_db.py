from app.internal.database.redis.redis_helper import RedisConnector, ModuleDB

redis_client = RedisConnector(module_db=ModuleDB.ASSETS_MANAGER)


async def create_dir_cache(key: str, value: str):
    test = redis_client.get_key("asd")
    print(test)


async def read_dir_cache(key: str):
    pass
