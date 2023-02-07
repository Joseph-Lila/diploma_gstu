from dataclasses import dataclass

from src.domain.commands.command import Command


@dataclass
class ImportWorkload(Command):
    path: str
