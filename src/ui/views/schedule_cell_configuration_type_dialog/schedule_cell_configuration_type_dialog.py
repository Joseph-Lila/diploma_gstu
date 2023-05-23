from kivy.uix.modalview import ModalView
from kivymd.uix.card import MDCard

from src.domain.entities import CellPart
from src.domain.enums import ViewState, WeekType, Subgroup


class ScheduleCellConfigurationTypeDialog(MDCard, ModalView):
    def __init__(self, slaves, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slaves = slaves

    def save_configuration_type(self, *args):
        chosen_ind = [
            elem.chosen
            for elem in (
                self.ids.btn_1,
                self.ids.btn_2,
                self.ids.btn_3,
                self.ids.btn_4,
                self.ids.btn_5,
                self.ids.btn_6,
                self.ids.btn_7,
                self.ids.btn_8,
            )
        ].index(True)
        # print(f"Выбрана конфигурация № {chosen_ind + 1}")
        self.dismiss()
