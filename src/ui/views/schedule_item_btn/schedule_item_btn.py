from kivy.properties import ObjectProperty
from kivy.uix.button import Button

from src.domain.interfaces import AbstractObserver
from src.ui.views.interfaces import AbstractSizeSlave


class ScheduleItemBtn(Button, AbstractSizeSlave, AbstractObserver):
    info = ObjectProperty()

    def on_press(self):
        pass

    def get_minimum_width(self):
        self.texture_update()
        return self.texture.size[0] + 18
