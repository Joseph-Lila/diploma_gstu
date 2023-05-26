from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.modalview import ModalView
from kivymd.uix.card import MDCard


class ScheduleCellContextMenu(MDCard, ModalView):
    clear_btn_event = ObjectProperty()
    pos_hint_x = NumericProperty(0.5)
    pos_hint_y = NumericProperty(0.5)

    def set_data(
        self,
        pos,
        pos_hint,
        clear_btn_event,
        clearable: bool,
    ):
        self.pos = pos
        self.pos_hint_x = pos_hint.get("x", 0.5)
        self.pos_hint_y = pos_hint.get("y", 0.5)

        if clearable:
            self.clear_btn_event = clear_btn_event
            self.ids.clear_btn.disabled = False
        else:
            self.clear_btn_event = lambda *args, **kwargs: None
            self.ids.clear_btn.disabled = True
