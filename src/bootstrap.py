import inspect

from kivy import Logger

from src import config
from src.adapters.orm.base import create_tables, init_database_with_data
from src.adapters.repositories.abstract_repository import AbstractRepository
from src.adapters.repositories.postgres_repository import PostgresRepository
from src.service_layer import handlers
from src.service_layer.messagebus import MessageBus


async def bootstrap(
    drop_create_tables: bool = False,
    init_database_data: bool = False,
    repository: AbstractRepository = PostgresRepository(),
    connection_string=config.get_postgres_uri(),
) -> MessageBus:
    if drop_create_tables:
        Logger.info("Application: Creating tables...")
        try:
            await create_tables(connection_string=connection_string)
        except:
            Logger.info("Application: Tables creation failed...")
            raise

    if init_database_data:
        Logger.info("Application: Filling tables with initial data...")
        try:
            await init_database_with_data(connection_string=connection_string)
        except:
            Logger.info("Application: Database initiation failed...")
            raise

    dependencies = {"repository": repository}
    injected_command_handlers = {
        command_type: inject_dependencies(handler, dependencies)
        for command_type, handler in handlers.COMMAND_HANDLERS.items()
    }

    return MessageBus(
        command_handlers=injected_command_handlers,
    )


def inject_dependencies(handler, dependencies):
    params = inspect.signature(handler).parameters
    deps = {
        name: dependency for name, dependency in dependencies.items() if name in params
    }
    return lambda message: handler(message, **deps)
