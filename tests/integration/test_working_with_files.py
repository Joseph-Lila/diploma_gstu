import asyncio

import pytest

from src.domain.entities import MentorLoadItem
from src.service_layer.handlers import write_mentor_load_items_to_csv, load_mentor_load_items_from_csv


@pytest.mark.asyncio
async def test_load_mentor_load_items_from_csv(csv_file_path):
    mentor_load_items = [
        MentorLoadItem("mentor1", 'group1', 'subject1', 'subject_type1', 1),
        MentorLoadItem("mentor2", 'group2', 'subject2', 'subject_type2', 2),
        MentorLoadItem("mentor3", 'group3', 'subject3', 'subject_type3', 3),
    ]
    await write_mentor_load_items_to_csv(csv_file_path, mentor_load_items)

    got_mentor_load_items = await load_mentor_load_items_from_csv(csv_file_path)

    assert mentor_load_items == got_mentor_load_items
