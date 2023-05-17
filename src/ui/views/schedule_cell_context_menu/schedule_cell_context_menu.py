from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.modalview import ModalView
from kivymd.uix.card import MDCard


class ScheduleCellContextMenu(MDCard, ModalView):
    tune_btn_event = ObjectProperty()
    clear_btn_event = ObjectProperty()
    pos_hint_x = NumericProperty(0.5)
    pos_hint_y = NumericProperty(0.5)

    def set_data(self, pos, pos_hint, tune_btn_event, clear_btn_event):
        self.pos = pos
        self.pos_hint_x = pos_hint["x"]
        self.pos_hint_y = pos_hint["y"]
        self.tune_btn_event = tune_btn_event
        self.clear_btn_event = clear_btn_event
