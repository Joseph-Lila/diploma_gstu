from kivy.uix.button import Button

from src.domain.interfaces import AbstractSizeSlave


class ScheduleItemBtn(Button, AbstractSizeSlave):
    def on_press(self):
        pass

    def get_minimum_width(self):
        self.texture_update()
        return self.texture.size[0] + 18
