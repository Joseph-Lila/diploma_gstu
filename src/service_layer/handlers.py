from dataclasses import astuple
from typing import Dict, Type, Callable, List

import aiofiles
from aiocsv import AsyncReader, AsyncWriter

from src.domain.commands import Command
from src.domain.entities import MentorLoadItem


async def load_mentor_load_items_from_csv(path: str) -> List[MentorLoadItem]:
    mentor_load_items: List[MentorLoadItem] = []
    async with aiofiles.open(
        path,
        mode='r',
        encoding='utf-8',
        newline='',
    ) as afp:
        async for row in AsyncReader(afp):
            mentor, group, subject, subject_type, hours = row
            item = MentorLoadItem(
                mentor,
                group,
                subject,
                subject_type,
                int(hours),
            )
            mentor_load_items.append(item)
    return mentor_load_items


async def write_mentor_load_items_to_csv(path: str, items: List[MentorLoadItem]):
    async with aiofiles.open(
        path,
        mode='w',
        encoding='utf-8',
        newline='',
    ) as afp:
        writer = AsyncWriter(afp, dialect='unix')
        for item in items:
            await writer.writerow(astuple(item))


COMMAND_HANDLERS = {

}  # type: Dict[Type[Command], Callable]
