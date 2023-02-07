from kivy.factory import Factory

from .main_screen import MainScreenView
from .vertical_label import VerticalLabel
from .start_screen import StartScreenView


Factory.register("MainScreenView", cls=MainScreenView)
Factory.register("VerticalLabel", cls=VerticalLabel)
Factory.register("StartScreenView", cls=StartScreenView)
