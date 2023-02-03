import asyncio
import concurrent.futures
import inspect

from src.adapters.repositories.abstract_repositories_manager import AbstractRepositoriesManager
from src.adapters.repositories.posgresql.repositories_manager import RepositoriesManager
from src.adapters.orm.base import create_tables
from src.service_layer import handlers
from src.service_layer.messagebus import MessageBus


def bootstrap(
        drop_create_tables: bool = False,
        repositories_manager: AbstractRepositoriesManager = RepositoriesManager(),
) -> MessageBus:

    if drop_create_tables:
        pool = concurrent.futures.ThreadPoolExecutor()
        pool.submit(asyncio.run, create_tables())

    dependencies = {"repositories_manager": repositories_manager}
    injected_command_handlers = {
        command_type: inject_dependencies(handler, dependencies)
        for command_type, handler in handlers.COMMAND_HANDLERS.items()
    }

    return MessageBus(
        repositories_manager=repositories_manager,
        command_handlers=injected_command_handlers,
    )


def inject_dependencies(handler, dependencies):
    params = inspect.signature(handler).parameters
    deps = {
        name: dependency
        for name, dependency in dependencies.items()
        if name in params
    }
    return lambda message: handler(message, **deps)
