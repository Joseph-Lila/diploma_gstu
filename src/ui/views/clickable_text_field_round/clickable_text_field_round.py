from typing import List

from kivy.properties import ObjectProperty, StringProperty
from kivymd.uix.card import MDCard
from kivymd.uix.menu import MDDropdownMenu


class ClickableTextFieldRound(MDCard):
    text = StringProperty()
    left_icon = StringProperty()
    right_icon = StringProperty()
    button_instance = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.menu = None

    def change_text_value(self, new_text: str):
        self.text = new_text
        self.menu.dismiss()

    async def bind_dropdown_menu(self, items: List[int]):
        options = [
            {
                "text": str(item),
                "viewclass": "OneLineListItem",
                "on_release": lambda x=str(item): self.change_text_value(x),
            }
            for item in items
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.right_icon_button,
            items=options,
            width_mult=2,
            max_height=250,
        )
        self.menu.open()
