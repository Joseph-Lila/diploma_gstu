from kivymd.uix.card import MDCard

from src.domain.enums import ViewType
from src.ui.views.schedule_week import ScheduleWeek


class GroupsSchedule(MDCard):
    def on_kv_post(self, base_widget):
        self.ids.groups_cont.add_widget(
            ScheduleWeek('IP-42', ViewType.GROUP.value, 6)
        )
