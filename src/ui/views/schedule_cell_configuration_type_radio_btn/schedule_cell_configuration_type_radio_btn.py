from kivy.properties import BooleanProperty, StringProperty
from kivymd.uix.card import MDCard


class ScheduleCellConfigurationTypeRadioBtn(MDCard):
    chosen = BooleanProperty()
    image_source = StringProperty()
