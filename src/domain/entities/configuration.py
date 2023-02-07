from typing import List

from src.domain.entities.mentor_load_item import MentorLoadItem


class Configuration:
    def __init__(self):
        self._mentor_load_items: List[MentorLoadItem] = []

    def add_mentor_load_item(self, mentor_load_item: MentorLoadItem):
        self._mentor_load_items.append(mentor_load_item)

    @property
    def mentor_load_items(self) -> List[MentorLoadItem]:
        return self._mentor_load_items

    @mentor_load_items.setter
    def mentor_load_items(self, value: List[MentorLoadItem]):
        self._mentor_load_items = value
