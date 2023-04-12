from typing import Callable, Type, Dict
from loguru import logger
from src.domain.events.event import Event


class ViewMessageBus:
    def __init__(
            self,
            main_view,
            event_handlers: Dict[Type[Event], Callable],
    ):
        self.main_view = main_view
        self.event_handlers: Dict[Type[Event], Callable] = event_handlers

    async def handle_event(self, event: Event):
        try:
            handler = self.event_handlers[type[event]]
            await handler(self.main_view, event)
        except Exception:
            logger.exception(f"Exception handling event {event}")
            raise
