import asyncio
import concurrent.futures
import inspect

from src.adapters.orm.base import create_tables
from src.adapters.repositories.abstract_repository import AbstractRepository
from src.adapters.repositories.postgres_repository import PostgresRepository
from src.service_layer import handlers
from src.service_layer.messagebus import MessageBus


def bootstrap(
    drop_create_tables: bool = False,
    repository: AbstractRepository = PostgresRepository(),
) -> MessageBus:
    if drop_create_tables:
        pool = concurrent.futures.ThreadPoolExecutor()
        pool.submit(asyncio.run, create_tables())

    dependencies = {"repository": repository}
    injected_command_handlers = {
        command_type: inject_dependencies(handler, dependencies)
        for command_type, handler in handlers.COMMAND_HANDLERS.items()
    }

    return MessageBus(
        repository=repository,
        command_handlers=injected_command_handlers,
    )


def inject_dependencies(handler, dependencies):
    params = inspect.signature(handler).parameters
    deps = {
        name: dependency for name, dependency in dependencies.items() if name in params
    }
    return lambda message: handler(message, **deps)
