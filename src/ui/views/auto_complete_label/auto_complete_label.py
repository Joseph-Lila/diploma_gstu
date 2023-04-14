from typing import List

from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivymd.uix.boxlayout import MDBoxLayout


class AutoCompleteLabel(MDBoxLayout):
    request_method = ObjectProperty()
    text = StringProperty()
    hint_text = StringProperty()
    total_width = NumericProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.opened = False

    def get_variants(self):
        if not self.opened:
            self.opened = True
            self.ids.rv.height = 100
            self.pos = self.pos[0], self.pos[1] - 100
            self.request_method(self)
        else:
            self.opened = False
            self._clear_variants()

    def _clear_variants(self):
        self.ids.rv.height = 0
        self.pos = self.pos[0], self.pos[1] + 100
        self.ids.rv.data = []

    def change_text_value_and_hide_options(self, new_value: str):
        self.opened = False
        self._clear_variants()
        self.change_text_value(new_value)

    def change_text_value(self, new_value: str):
        self.ids.label.text = new_value

    def _add_variant(self, variant: str):
        self.ids.rv.data.append(
            {
                "viewclass": "OneLineListItem",
                "text": variant,
                "on_press": lambda x=variant: self.change_text_value_and_hide_options(x),
            }
        )

    async def update_variants(self, collection: List[str]):
        for element in collection:
            self._add_variant(element)
