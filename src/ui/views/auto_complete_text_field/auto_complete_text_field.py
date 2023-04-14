from typing import List

from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivymd.uix.boxlayout import MDBoxLayout


class AutoCompleteTextField(MDBoxLayout):
    request_method = ObjectProperty()
    hint_text = StringProperty()
    total_width = NumericProperty()
    input_filter = ObjectProperty()

    def get_variants(self, text=''):
        if self.ids.search_field.focus is False:
            self._clear_variants()
        else:
            self.request_method(self, text)

    def _clear_variants(self):
        self.ids.rv.data = []

    def _change_text_value(self, new_value: str):
        self.ids.search_field.text = new_value

    def _add_variant(self, variant: str):
        self.ids.rv.data.append(
            {
                "viewclass": "OneLineListItem",
                "text": variant,
                "on_press": lambda x=variant: self._change_text_value(x),
            }
        )

    async def update_variants(self, collection: List[str]):
        self._clear_variants()
        for element in collection:
            self._add_variant(element)
