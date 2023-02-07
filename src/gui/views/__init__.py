from kivy.factory import Factory

from .configuration_description_screen import \
    ConfigurationDescriptionScreenView
from .custom_text_input import CustomTextInput
from .main_screen import MainScreenView
from .start_screen import StartScreenView
from .vertical_label import VerticalLabel

Factory.register("MainScreenView", cls=MainScreenView)
Factory.register("VerticalLabel", cls=VerticalLabel)
Factory.register("StartScreenView", cls=StartScreenView)
Factory.register("ConfigurationScreenView", cls=ConfigurationDescriptionScreenView)
Factory.register("CustomTextInput", cls=CustomTextInput)
