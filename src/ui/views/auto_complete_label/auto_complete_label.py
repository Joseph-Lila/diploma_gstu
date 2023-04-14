from typing import List

from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivymd.uix.boxlayout import MDBoxLayout


class AutoCompleteLabel(MDBoxLayout):
    request_method = ObjectProperty()
    hint_text = StringProperty()
    total_width = NumericProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.opened = False

    def get_variants(self):
        if not self.opened:
            self.opened = True
            self.request_method(self, '')
        else:
            self.opened = False
            self._clear_variants()

    def _clear_variants(self):
        self.ids.rv.data = []

    def _change_text_value(self, new_value: str):
        self.ids.label.text = new_value

    def _add_variant(self, variant: str):
        self.ids.rv.data.append(
            {
                "viewclass": "OneLineListItem",
                "text": variant,
                "on_press": lambda x=variant: self._change_text_value(x),
            }
        )

    def update_variants(self, collection: List[str]):
        self._clear_variants()
        for element in collection:
            self._add_variant(element)
