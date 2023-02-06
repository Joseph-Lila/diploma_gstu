from kivy.factory import Factory

from .main_screen import MainScreenView
from .vertical_label import VerticalLabel


Factory.register("MainScreenView", cls=MainScreenView)
Factory.register("VerticalLabel", cls=VerticalLabel)
