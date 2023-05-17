from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu
from .menu_header import MenuHeader


class ScheduleCellContextMenu:
    @staticmethod
    def get_menu_items(owner):
        return [
            {
                "text": "Настроить компоновку",
                "viewclass": "OneLineListItem",
                "height": dp(56),
                "on_release": owner.open_dialog
            },
            {
                "text": "Очистить ячейку",
                "viewclass": "OneLineListItem",
                "height": dp(56),
                "on_release": owner.clear
            }
        ]

    @staticmethod
    def get_menu(owner):
        menu_items = ScheduleCellContextMenu.get_menu_items(owner)
        menu = MDDropdownMenu(
            header_cls=MenuHeader(),
            caller=owner,
            items=menu_items,
            width_mult=4,
        )
        return menu
