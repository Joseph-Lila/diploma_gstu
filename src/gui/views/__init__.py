from kivy.factory import Factory

from .main_screen import MainScreenView
from .vertical_label import VerticalLabel
from .start_screen import StartScreenView
from .configuration_description_screen import ConfigurationDescriptionScreenView


Factory.register("MainScreenView", cls=MainScreenView)
Factory.register("VerticalLabel", cls=VerticalLabel)
Factory.register("StartScreenView", cls=StartScreenView)
Factory.register("ConfigurationScreenView", cls=ConfigurationDescriptionScreenView)
