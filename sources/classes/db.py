"""Provides generic methods to interact with DB."""

import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, insert, MetaData, Table
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import OperationalError
from sources.utilities import display, logs
from sources.models.project import Project
from sources.models.user import User

load_dotenv()
Base = declarative_base()


class Client:
    """Database Client class."""

    def __init__(self) -> None:
        """Client Constructor."""
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")
        self.user = os.getenv("DB_USERNAME")
        self.passwd = os.getenv("DB_PASSWORD")
        self.dbname = os.getenv("DB_DATABASE")
        self.engine = None

    def get_engine(self) -> object:
        """Get database engine."""
        if self.engine is None:
            self.connection()
        return self.engine

    def set_engine(self, engine: object) -> None:
        """Set database engine."""
        if engine is not None:
            self.engine = engine
        else:
            self.engine = self.connection()

    def unset_engine(self) -> None:
        """Unset database engine."""
        self.engine = None

    def connection(self):
        """Connect to database."""
        driver = "postgresql+psycopg"
        engine = create_engine(
            f"{driver}://{self.user}:{self.passwd}@{self.host}:{self.port}/{self.dbname}"
        )

        try:
            with engine.connect():
                logs.get_logger().info(
                    "Successfully connected to the PostgreSQL database %s for user %s",
                    self.dbname,
                    self.user,
                )
                self.set_engine(engine)
        except OperationalError as exc:
            logs.get_logger().error(
                "An error occurred when connecting database: %s", exc
            )
            sys.exit(display.alert("Failed to connect to database: " + repr(exc)))

        return engine

    def close_connection(self, engine: object) -> None:
        """Close database connection."""
        engine.dispose()
        self.unset_engine()
        logs.get_logger().info("Connection to database closed")

    def create_schema(self, engine: object) -> None:
        """Create database schema."""
        Project.metadata.create_all(engine)
        User.metadata.create_all(engine)

    def drop_schema(self, engine: object):
        """Drop database schema."""
        metadata = MetaData()
        metadata.reflect(bind=engine)
        metadata.drop_all(bind=engine)

    def write_data(self, engine: object, table_name: str, data: object):
        """Write data into database."""
        tbl = Table(table_name, MetaData(), autoload_with=engine)
        with engine.connect() as connection:
            insert_request = insert(tbl).values(data)
            connection.execute(insert_request)
            connection.commit()

    def debug_tables_list(self, engine: object):
        """List all tables in the database."""
        logs.get_logger().info("List tables in database")
        metadata = MetaData()
        metadata.reflect(bind=engine)
        return [table.name for table in metadata.tables.values()]
