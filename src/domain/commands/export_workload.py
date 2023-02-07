from dataclasses import dataclass
from typing import List

from src.domain.commands.command import Command
from src.domain.entities import MentorLoadItem


@dataclass
class ExportWorkload(Command):
    path: str
    mentor_load_items: List[MentorLoadItem]
