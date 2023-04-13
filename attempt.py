from typing import Callable, List

from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen

from kivymd.icon_definitions import md_icons
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout

Builder.load_string(
'''
#:import images_path kivymd.images_path

<AutoCompleteTextField>:
    orientation: 'vertical'
    
    MDTextField:
        id: search_field
        adaptive_size: True
        hint_text: 'Search icon'
        on_text: root.get_variants(self.text)
        on_focus: root.get_variants(self.text)
    
    MDRecycleView:
        id: rv
        key_viewclass: 'viewclass'
        key_size: 'height'
    
        MDRecycleGridLayout:
            padding: dp(10)
            default_size: None, dp(48)
            default_size_hint: 1, None
            adaptive_height: True
            cols: 1
            md_bg_color: 'pink'
                 
                    
<PreviousMDIcons>:

    MDBoxLayout:
        orientation: 'vertical'
        padding: 10
        spacing: 10
            
        AutoCompleteTextField:
        
        Button:
 '''
)


def my_request_method(auto_complete_widget_instance, text, *args):
    answer = [r for r in md_icons.keys() if text in r]
    auto_complete_widget_instance.update_variants(answer)


class AutoCompleteTextField(MDBoxLayout):
    request_method = my_request_method

    def get_variants(self, instance_text_field, text=''):
        if self.ids.search_field.focus is False:
            self._clear_variants()
        else:
            self.request_method(instance_text_field, text)

    def _clear_variants(self):
        self.ids.rv.data = []

    def _change_text_value(self, new_value: str):
        self.ids.search_field.text = new_value

    def _add_variant(self, variant: str):
        self.ids.rv.data.append(
            {
                "viewclass": "OneLineListItem",
                "text": variant,
                "on_press": lambda x=variant: self._change_text_value(x),
            }
        )

    def update_variants(self, collection: List[str]):
        self._clear_variants()
        for element in collection:
            self._add_variant(element)


class PreviousMDIcons(Screen):
    pass


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = PreviousMDIcons()

    def build(self):
        return self.screen


MainApp().run()
