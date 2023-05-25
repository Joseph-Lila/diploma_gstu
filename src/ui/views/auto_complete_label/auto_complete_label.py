from typing import List

from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivymd.uix.boxlayout import MDBoxLayout

from src.ui.views.interfaces import AbstractAutoCompleteElement


class AutoCompleteLabel(MDBoxLayout, AbstractAutoCompleteElement):
    request_method = ObjectProperty()
    change_text_request = ObjectProperty()
    text = StringProperty()
    hint_text = StringProperty()
    total_width = NumericProperty()
    recycle_view_height = NumericProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.entity = None
        self.opened = False

    def get_variants(self):
        if not self.opened:
            self.opened = True
            self.ids.rv.height = self.recycle_view_height
            self.pos = self.pos[0], self.pos[1] - self.recycle_view_height
            self.request_method(self)
        else:
            self.opened = False
            self._clear_variants()

    def _clear_variants(self):
        self.ids.rv.height = 0
        self.pos = self.pos[0], self.pos[1] + self.recycle_view_height
        self.ids.rv.data = []

    def change_text_value_and_hide_options(self, new_value: str):
        self.opened = False
        self._clear_variants()
        self.change_text_value(new_value)

    def change_text_value(self, new_value: str):
        self.ids.label.text = new_value

        if self.change_text_request is not None:
            self.change_text_request()

    def _add_variant(self, variant: str):
        self.ids.rv.data.append(
            {
                "viewclass": "OneLineListItem",
                "text": variant,
                "bg_color": (185 / 255, 162 / 255, 255 / 255, 100 / 100),
                "divider_color": "white",
                "on_press": lambda x=variant: self.change_text_value_and_hide_options(x),
            }
        )

    def change_entity(self, entity):
        self.entity = entity

    def _add_entity(self, entity, key_: str):
        self.ids.rv.data.append(
            {
                "viewclass": "OneLineListItem",
                "text": getattr(entity, key_),
                "bg_color": (185 / 255, 162 / 255, 255 / 255, 100 / 100),
                "divider_color": "white",
                "on_press": lambda x=getattr(entity, key_): self.change_text_value_and_hide_options(x),
                "on_release": lambda x=entity: self.change_entity(x),
            }
        )

    async def update_variants(self, collection: List[str]):
        for element in collection:
            self._add_variant(element)

    async def update_entities(self, collection: list, key_):
        for element in collection:
            self._add_entity(element, key_)
