from kivy.properties import StringProperty
from kivymd.uix.card import MDCard

from src.domain.enums import DayOfWeek, ViewType
from src.domain.interfaces import AbstractSizeMaster
from src.ui.views.schedule_day import ScheduleDay


class ScheduleWeek(MDCard, AbstractSizeMaster):
    view_type = StringProperty()

    def __init__(
            self,
            entity_title: str,
            view_type: str,
            pairs_quantity: int,
            *args,
            **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.slaves = []
        self.update_metadata(entity_title, view_type, pairs_quantity)

    def update_metadata(
            self,
            entity_title: str,
            view_type: str,
            pairs_quantity: int,
    ):
        self.ids.entity_title.text = entity_title
        self.view_type = view_type
        self.ids.cont.clear_widgets()
        self.slaves = [
            ScheduleDay(
                pairs_quantity,
                day_of_week.value,
                cur_group=entity_title if view_type == ViewType.GROUP.value else '',
            )
            for day_of_week in DayOfWeek
        ]
        for slave in self.slaves:
            self.ids.cont.add_widget(slave)
        self.fit_slaves()
        self.ids.entity_title.width = self.slaves[-1].width
        self.width = self.slaves[-1].width
