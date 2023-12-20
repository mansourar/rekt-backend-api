from functools import wraps

from app.exceptions import *
from app.internal.helpers.components.environment import Environment

GLOBAL_ENV = Environment()


def server_auth_required(func):
    @wraps(func)
    async def wrapper(**kwargs):
        if "cred" not in kwargs:
            raise ServerAuthorizationMissingException("No 'cred' argument provided")
        if not await private_api_basic_auth(kwargs["cred"]):
            raise InvalidServerAuthorizationException("Invalid Server Credentials")
        return await func(**kwargs)

    return wrapper


async def private_api_basic_auth(credentials):
    username = getattr(GLOBAL_ENV, "PRIVATE_API_USERNAME", "")
    password = getattr(GLOBAL_ENV, "PRIVATE_API_PASSWORD", "")
    is_user_ok = credentials.username == username
    is_pass_ok = credentials.password == password
    return is_user_ok and is_pass_ok


def client_auth_required(func):
    @wraps(func)
    async def wrapper(**kwargs):
        pass

    return wrapper
