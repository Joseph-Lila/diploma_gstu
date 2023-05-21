from kivy.uix.modalview import ModalView
from kivymd.uix.card import MDCard


class ScheduleItemDialog(MDCard, ModalView):
    def __init__(self, touched_slave, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.touched_slave = touched_slave

        self.set_info_records()

    def get_info_records(self):
        pass

    def set_info_records(self):
        self.ids.lbl.text = f"{self.touched_slave}"
