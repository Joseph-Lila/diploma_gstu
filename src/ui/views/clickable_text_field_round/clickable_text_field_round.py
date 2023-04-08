from kivy.properties import StringProperty, ObjectProperty
from kivymd.uix.card import MDCard


class ClickableTextFieldRound(MDCard):
    text = StringProperty()
    left_icon = StringProperty()
    right_icon = StringProperty()
    button_instance = ObjectProperty()
