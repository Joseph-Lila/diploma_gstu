from kivy.app import App
from kivy.uix.modalview import ModalView
from kivymd.uix.card import MDCard

from src.domain.entities import CellPart
from src.domain.enums import ViewState, WeekType, Subgroup


class ScheduleCellConfigurationTypeDialog(MDCard, ModalView):
    CONFIGURATION_VIEW_STATES = {
        1: (1, 1, 1, 1),
        2: (1, 0, 1, 1),
        3: (1, 1, 1, 0),
        4: (1, 1, 1, 1),
        5: (1, 1, 1, 1),
        6: (1, 0, 1, 0),
        7: (1, 1, 0, 0),
        8: (1, 0, 0, 0),
    }
    CONFIGURATION_CELL_PARTS = {
        1: (
            (WeekType.ABOVE.value, Subgroup.FIRST.value),
            (WeekType.ABOVE.value, Subgroup.SECOND.value),
            (WeekType.UNDER.value, Subgroup.FIRST.value),
            (WeekType.UNDER.value, Subgroup.SECOND.value),
        ),
        2: (
            (WeekType.ABOVE.value, Subgroup.BOTH.value),
            (WeekType.UNDEFINED.value, Subgroup.UNDEFINED.value),
            (WeekType.UNDER.value, Subgroup.FIRST.value),
            (WeekType.UNDER.value, Subgroup.SECOND.value),
        ),
        3: (
            (WeekType.ABOVE.value, Subgroup.FIRST.value),
            (WeekType.ABOVE.value, Subgroup.SECOND.value),
            (WeekType.UNDER.value, Subgroup.BOTH.value),
            (WeekType.UNDEFINED.value, Subgroup.UNDEFINED.value),
        ),
        4: (
            (WeekType.BOTH.value, Subgroup.FIRST.value),
            (WeekType.ABOVE.value, Subgroup.SECOND.value),
            (WeekType.BOTH.value, Subgroup.FIRST.value),
            (WeekType.UNDER.value, Subgroup.SECOND.value),
        ),
        5: (
            (WeekType.ABOVE.value, Subgroup.FIRST.value),
            (WeekType.BOTH.value, Subgroup.SECOND.value),
            (WeekType.UNDER.value, Subgroup.FIRST.value),
            (WeekType.BOTH.value, Subgroup.SECOND.value),
        ),
        6: (
            (WeekType.ABOVE.value, Subgroup.BOTH.value),
            (WeekType.UNDEFINED.value, Subgroup.UNDEFINED.value),
            (WeekType.UNDER.value, Subgroup.BOTH.value),
            (WeekType.UNDEFINED.value, Subgroup.UNDEFINED.value),
        ),
        7: (
            (WeekType.BOTH.value, Subgroup.FIRST.value),
            (WeekType.BOTH.value, Subgroup.SECOND.value),
            (WeekType.UNDEFINED.value, Subgroup.UNDEFINED.value),
            (WeekType.UNDEFINED.value, Subgroup.UNDEFINED.value),
        ),
        8: (
            (WeekType.BOTH.value, Subgroup.BOTH.value),
            (WeekType.UNDEFINED.value, Subgroup.UNDEFINED.value),
            (WeekType.UNDEFINED.value, Subgroup.UNDEFINED.value),
            (WeekType.UNDEFINED.value, Subgroup.UNDEFINED.value),
        ),
    }

    def __init__(self, slaves, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slaves = slaves

    def save_configuration_type(self, *args):
        chosen_ind = [
            elem.chosen
            for elem in (
                self.ids.btn_1,
                self.ids.btn_2,
                self.ids.btn_3,
                self.ids.btn_4,
                self.ids.btn_5,
                self.ids.btn_6,
                self.ids.btn_7,
                self.ids.btn_8,
            )
        ].index(True)
        print(f"Выбрана конфигурация № {chosen_ind + 1}")
        self.tune_configuration(chosen_ind)
        App.get_running_app().root.get_current_screen_view().fit_store_widgets()
        self.dismiss()

    def tune_configuration(self, number):
        for i, slave in enumerate(self.slaves):
            slave.schedule_item_info.cell_part = CellPart(
                *self.CONFIGURATION_CELL_PARTS[number][i]
            )

            if self.CONFIGURATION_VIEW_STATES[number][i] != 0:
                # TODO: define real view_state
                view_state = ViewState.EMPTY.value
            else:
                view_state = ViewState.INVISIBLE.value
            slave.update_view_metadata(view_state=view_state)
