from typing import Callable, Dict, Type

from loguru import logger

from src.adapters.repositories.abstract_repositories_manager import \
    AbstractRepositoriesManager
from src.domain.commands.command import Command


class MessageBus:
    def __init__(
            self,
            repositories_manager: AbstractRepositoriesManager,
            command_handlers: Dict[Type[Command], Callable]
    ):
        self.repositories_manager = repositories_manager
        self.command_handlers = command_handlers

    async def handle_command(self, command: Command):
        try:
            handler = self.command_handlers[type(command)]
            return await handler(command)
        except Exception:
            logger.exception(f"Exception handling command {command}")
            raise
