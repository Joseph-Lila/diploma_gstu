import functools

import asyncio

from kivy.factory import Factory

from src.domain.commands.command import Command
from src.domain.events.event import Event
from src.service_layer.messagebus import MessageBus
from src.ui.view_messagebus import ViewMessageBus


async def do_with_loading_modal_view(func, *args, **kwargs):
    loading_modal_view = Factory.LoadingModalView()
    loading_modal_view.open()
    await func(*args, **kwargs)
    loading_modal_view.dismiss()


def use_loop(func):
    @functools.wraps(func)
    async def wrapped(self, *args, **kwargs):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            loop.create_task(func(self, *args, **kwargs))

    return wrapped


class Controller:
    def __init__(self, model: MessageBus):
        self.model: MessageBus = model

    @use_loop
    async def process_command(self, sender: ViewMessageBus, cmd: Command):
        event: Event = await self.model.handle_command(cmd)
        await sender.handle_event(event)

    @use_loop
    async def process_event(self, sender: ViewMessageBus, event: Event):
        await sender.handle_event(event)
