from kivymd.uix.textfield import MDTextField


class CustomTextInput(MDTextField):
    def set_objects_labels(self) -> None:
        super().set_objects_labels()
        self._hint_text_label.font_name = "assets/fonts/MontserratAlternates-Bold.otf"
