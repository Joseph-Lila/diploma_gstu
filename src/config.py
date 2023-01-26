""" Module srс """
import pathlib
from dotenv import load_dotenv
import os


THIS_DIR = pathlib.Path(__file__).parent.resolve().absolute()
ROOT_DIR = THIS_DIR.parent
DOTENV_PATH = ROOT_DIR / '.env'


# load secret data from .env
if DOTENV_PATH.exists():
    load_dotenv(DOTENV_PATH)


def get_test_postgres_url() -> str:
    """
    Method to get connection string for testing PostgreSQl server.
    :return: str: connection string.
    """
    host = os.environ.get('POSTGRESQL_TEST_HOST')
    port = os.environ.get('POSTGRESQL_TEST_PORT')
    password = os.environ.get('POSTGRESQL_TEST_PASSWORD')
    user = os.environ.get('POSTGRESQL_TEST_USERNAME')
    db_name = os.environ.get('POSTGRESQL_TEST_MAINTENANCE_DATABASE')
    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}"
