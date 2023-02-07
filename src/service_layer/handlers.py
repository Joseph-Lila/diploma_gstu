from dataclasses import astuple
from typing import Callable, Dict, List, Type

import aiofiles
from aiocsv import AsyncReader, AsyncWriter

from src.domain.commands import ExportWorkload, ImportWorkload
from src.domain.commands.command import Command
from src.domain.entities import MentorLoadItem
from src.domain.events import WorkloadIsExported, WorkloadIsImported


async def import_workload(
        cmd: ImportWorkload,
):
    mentor_load_items = await load_mentor_load_items_from_csv(cmd.path)
    return WorkloadIsImported(mentor_load_items=mentor_load_items)


async def export_workload(
        cmd: ExportWorkload,
):
    await write_mentor_load_items_to_csv(cmd.path, cmd.mentor_load_items)
    return WorkloadIsExported()


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
    ImportWorkload: import_workload,
    ExportWorkload: export_workload,
}  # type: Dict[Type[Command], Callable]
