from typing import Callable, Dict, Type

from loguru import logger

from src.adapters.repositories.abstract_repository import AbstractRepository
from src.domain.commands.command import Command


class MessageBus:
    def __init__(
        self,
        repository: AbstractRepository,
        command_handlers: Dict[Type[Command], Callable],
    ):
        self.repository = repository
        self.command_handlers = command_handlers

    async def handle_command(self, command: Command):
        try:
            handler = self.command_handlers[type(command)]
            return await handler(command)
        except Exception:
            logger.exception(f"Exception handling command {command}")
            raise
