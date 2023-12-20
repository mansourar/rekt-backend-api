import logging
import os

from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)


class PgsqlBase:
    BASE = declarative_base()
    ENGINE = None
    META = None
    SESSION_MAKER = None

    def __init__(self, host_env_var):
        self.connection_string = None
        self.host_env_var = host_env_var
        self.set_connection_string()

    def set_connection_string(self):
        host = os.getenv(self.host_env_var)
        port = os.getenv("PGSQL_PORT")
        pwd = os.getenv("PGSQL_PASS")
        user = os.getenv("PGSQL_USER")
        db_name = os.getenv("PGSQL_DB_NAME")
        self.connection_string = f"postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{db_name}"

    def setup_pgsql_connection(self, check_session: bool):
        session = None
        if os.getenv(self.host_env_var) is None:
            return "Invalid Database Environment Variables"
        try:
            connection_type = type(self)
            connection_type.ENGINE = create_engine(
                self.connection_string,
                echo=False,
                pool_size=20,
                pool_recycle=3600,
                isolation_level="READ COMMITTED",
                execution_options={"postgresql_on_conflict": "raise"},
            )
            connection_type.ENGINE.connect()
            connection_type.META = MetaData(schema="public")
            connection_type.META.reflect(bind=connection_type.ENGINE)
            connection_type.SESSION_MAKER = sessionmaker(bind=self.ENGINE)

            if check_session:
                session = connection_type.SESSION_MAKER()

        except Exception as exc:
            logger.critical(str(exc))
            return f"Invalid pgsql Connection String {str(exc)}"
        finally:
            if session is not None:
                session.close()
        return None


class PgsqlWriter(PgsqlBase):
    def __init__(self):
        super().__init__("PGSQL_WRITER_HOST")


class PgsqlReader(PgsqlBase):
    def __init__(self):
        super().__init__("PGSQL_READER_HOST")
