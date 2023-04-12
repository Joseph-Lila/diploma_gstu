from typing import List
import asynckivy as ak
from kivy.uix.modalview import ModalView
from kivymd.uix.card import MDCard
from src.adapters.orm import Schedule
from src.ui.views.schedule_list_item import ScheduleListItem


class OpenDialog(MDCard, ModalView):
    async def update_items(self, new_items: List[Schedule]):
        self.ids.list_container.clear_widgets()
        for item in new_items:
            self.ids.list_container.add_widget(
                ScheduleListItem(schedule_item=item)
            )
