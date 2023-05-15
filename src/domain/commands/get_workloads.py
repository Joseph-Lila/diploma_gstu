from dataclasses import dataclass

from src.domain.commands.command import Command


@dataclass
class GetWorkloads(Command):
    group_substring: str
    subject_substring: str
    subject_type_substring: str
    mentor_substring: str
    year: int
    term: str
