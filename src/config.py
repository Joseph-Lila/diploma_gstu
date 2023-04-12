""" Module srс """
import os
import pathlib

from dotenv import load_dotenv

THIS_DIR = pathlib.Path(__file__).parent.resolve().absolute()
ROOT_DIR = THIS_DIR.parent
DOTENV_PATH = ROOT_DIR / '.env'
COMMON_WINDOW_SIZE = 878, 515


# load secret data from .env
if DOTENV_PATH.exists():
    load_dotenv(DOTENV_PATH)


def get_common_window_size():
    return COMMON_WINDOW_SIZE


def get_pairs_quantity() -> int:
    return os.environ.get('PAIRS_QUANTITY', 6)


def get_test_postgres_uri() -> str:
    """
    Method to get connection string for testing PostgreSql server.
    :return: str: connection string.
    """
    host = os.environ['POSTGRESQL_TEST_HOST']
    port = os.environ['POSTGRESQL_TEST_PORT']
    password = os.environ['POSTGRESQL_TEST_PASSWORD']
    user = os.environ['POSTGRESQL_TEST_USERNAME']
    db_name = os.environ['POSTGRESQL_TEST_MAINTENANCE_DATABASE']
    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}"


def get_postgres_uri() -> str:
    """
    Method to get connection string for PostgreSql server.
    :return: str: connection string.
    """
    host = os.environ['POSTGRESQL_HOST']
    port = os.environ['POSTGRESQL_PORT']
    password = os.environ['POSTGRESQL_PASSWORD']
    user = os.environ['POSTGRESQL_USERNAME']
    db_name = os.environ['POSTGRESQL_MAINTENANCE_DATABASE']
    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}"
