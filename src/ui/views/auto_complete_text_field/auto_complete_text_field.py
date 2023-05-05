from typing import List

from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivymd.uix.boxlayout import MDBoxLayout

from src.ui.views.interfaces import AbstractAutoCompleteElement


class AutoCompleteTextField(MDBoxLayout, AbstractAutoCompleteElement):
    request_method = ObjectProperty()
    change_text_request = ObjectProperty()
    text = StringProperty()
    hint_text = StringProperty()
    total_width = NumericProperty()
    input_filter = ObjectProperty()
    recycle_view_height = NumericProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.opened = False
        self.skip_manipulation = False

    def get_variants_using_focus(self, text=""):
        if self.ids.search_field.focus:
            self.request_method(self, text)
            self.opened = True
        else:
            self._clear_variants()
            self.opened = False

    def get_variants_using_text(self, text=""):
        if self.skip_manipulation:
            self.skip_manipulation = False
            return

        if self.opened:
            self._clear_variants()
            self.request_method(self, text)

    def _clear_variants(self):
        self.ids.rv.height = 0
        self.pos = self.pos[0], self.pos[1] + self.recycle_view_height
        self.ids.rv.data = []

    def change_text_value(self, new_value: str):
        self.skip_manipulation = True
        self.ids.search_field.text = new_value

        if self.change_text_request is not None:
            self.change_text_request()

    def _add_variant(self, variant: str):
        self.ids.rv.data.append(
            {
                "viewclass": "OneLineListItem",
                "text": variant,
                "bg_color": (185 / 255, 162 / 255, 255 / 255, 100 / 100),
                "divider_color": "white",
                "on_press": lambda x=variant: self.change_text_value(x),
            }
        )

    async def update_variants(self, collection: List[str]):
        self.ids.rv.height = self.recycle_view_height
        self.pos = self.pos[0], self.pos[1] - self.recycle_view_height
        for element in collection:
            self._add_variant(element)
