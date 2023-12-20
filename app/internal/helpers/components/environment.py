import os
from enum import Enum

from dotenv import load_dotenv

ENV_LOCAL = "local"
ENV_TEST = "test"
ENV_PROD = "production"
ENV_DEV = "development"

LOCAL_ENVIRONMENTS = [ENV_LOCAL, ENV_TEST]
PUBLIC_ENVIRONMENTS = [ENV_PROD, ENV_DEV]


class Environments(Enum):
    LOCAL = 0
    TEST = 1
    DEV = 2
    PROD = 3


ENVIRONMENT_KEYS = {
    "ENV": "pdtl",
    "CONSOLE_LOGGER": "pdtl",
    "FILE_LOGGER": "pdtl",
    "PRIVATE_API_USERNAME": "pdtl",
    "PRIVATE_API_PASSWORD": "pdtl",
    "PGSQL_WRITER_HOST": "pdtl",
    "PGSQL_READER_HOST": "pdtl",
    "PGSQL_PORT": "pdtl",
    "PGSQL_USER": "pdtl",
    "PGSQL_PASS": "pdtl",
    "PGSQL_DB_NAME": "pdtl",
    "AWS_ACCESS_KEY_ID": "pdtl",
    "AWS_SECRET_ACCESS_KEY": "pdtl"
}


def convert_permission_to_binary(permission: str):
    result = ""

    if "l" in permission:
        result = result + "1"
    else:
        result = result + "0"

    if "t" in permission:
        result = result + "1"
    else:
        result = result + "0"

    if "d" in permission:
        result = result + "1"
    else:
        result = result + "0"

    if "p" in permission:
        result = result + "1"
    else:
        result = result + "0"

    return result


class Environment:
    _instance = None

    def __new__(cls, reload=False):
        if reload or cls._instance is None:
            cls._instance = super(Environment, cls).__new__(cls)
            cls._instance.__init__(reload=reload)
        return cls._instance

    def __init__(self, reload=False):
        if reload or not hasattr(self, "initialized"):
            self._initialize()
            self.initialized = True

    def _initialize(self):
        load_dotenv()
        match os.getenv("ENV", ""):
            case "local":
                self.env = Environments.LOCAL
                self.is_local = True
            case "test":
                self.env = Environments.TEST
                self.is_local = True
            case "development":
                self.env = Environments.DEV
                self.is_local = False
            case "production":
                self.env = Environments.PROD
                self.is_local = False
            case _:
                raise EnvironmentError("Invalid Environment Type")

        for key, permission_level in ENVIRONMENT_KEYS.items():
            bin_representation = convert_permission_to_binary(str(permission_level))
            if int(bin_representation[self.env.value]) == 1:
                if key not in os.environ:
                    raise EnvironmentError(key)
                setattr(self, key, os.environ[key])
