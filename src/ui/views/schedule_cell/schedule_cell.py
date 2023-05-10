from kivymd.uix.card import MDCard

from src.domain.interfaces import AbstractSizeMaster, AbstractSizeSlave


class ScheduleCell(MDCard, AbstractSizeMaster, AbstractSizeSlave):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slaves = []

    def add_slaves(self, slaves):
        if len(slaves) != 4:
            raise
        self.slaves.extend(slaves)
        self.ids.top_cont.add_widget(slaves[0])
        self.ids.top_cont.add_widget(slaves[1])
        self.ids.bottom_cont.add_widget(slaves[2])
        self.ids.bottom_cont.add_widget(slaves[3])

    def get_minimum_width(self):
        self.texture_update()
        return self.width
