import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI

from app.internal.database.postgres.pgsql_helper import PgsqlReader, PgsqlWriter
from app.internal.database.s3.s3_client import S3Client
from app.internal.helpers.components.environment import Environment, convert_permission_to_binary
from app.routers import server, assets_manager

load_dotenv()
GLOBAL_ENV = Environment()

ENVIRONMENT_ROUTERS = [
    {
        "router": server.router,
        "description": "Server Actions & Health Checks",
        "permissions": "pdtl",
    },
    {
        "router": assets_manager.router,
        "description": "Assets Manager",
        "permissions": "pdtl"
    }
]


def environment_setup():
    load_dotenv()

    logging.info("Validating PgSql Writer Connection")
    pgsql = PgsqlWriter()
    pgsql_error = pgsql.setup_pgsql_connection(check_session=True)
    if pgsql_error is not None:
        logging.critical(f"Unable To Connect To MySql (Writer): {pgsql_error}")
        exit()

    logging.info("Validating PgSql Reader Connection")
    pgsql = PgsqlReader()
    pgsql_error = pgsql.setup_pgsql_connection(check_session=True)
    if pgsql_error is not None:
        logging.critical(f"Unable To Connect To MySql (Reader): {pgsql_error}")
        exit()

    logging.info("Validating S3 Buckets")
    s3_client = S3Client()
    result, error = s3_client.environment_bucket_check()
    if error:
        logging.critical(f"S3 Bucket Verification Error {error}")
        exit()

    # TODO: Validate DYNAMODB


app = FastAPI(
    title=f"Backend Services [{os.getenv('ENV')}]",
    description=f"**{os.getenv('AB_BASE_URL')}**",
    version="0.0.1"
)

for row in ENVIRONMENT_ROUTERS:
    permission_level = row["permissions"]
    router = row["router"]
    description = row["description"]
    bin_representation = convert_permission_to_binary(permission_level)
    if int(bin_representation[GLOBAL_ENV.env.value]) == 1:
        app.include_router(router, prefix="/api", tags=[description])


@app.on_event("startup")
async def startup_event():
    environment_setup()
