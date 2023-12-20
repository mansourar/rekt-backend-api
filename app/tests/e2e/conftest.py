import pytest
from starlette.testclient import TestClient

from app.internal.database.postgres.pgsql_helper import PgsqlReader, PgsqlWriter
from app.main import environment_setup


@pytest.fixture(scope="session")
def client():
    from app.main import app

    setup_postgres_connection()
    environment_setup()

    clear_db_state()
    yield TestClient(app)
    clear_db_state()


def setup_postgres_connection():
    pgsql = PgsqlWriter()
    pgsql.setup_pgsql_connection(check_session=False)

    pgsql = PgsqlReader()
    pgsql.setup_pgsql_connection(check_session=False)


def teardown_pgdb():
    # with PgsqlWriter.SESSION_MAKER() as psql_session:
    # stmt = text(f'TRUNCATE "{ReplaySession.__tablename__}" CASCADE')
    # psql_session.execute(stmt)
    pass


def teardown_redis():
    pass


def teardown_dynamo_db():
    pass


def clear_db_state():
    teardown_redis()
    teardown_pgdb()
    teardown_dynamo_db()
