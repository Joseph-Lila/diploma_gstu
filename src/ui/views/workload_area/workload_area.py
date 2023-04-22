from kivymd.uix.card import MDCard


class WorkloadArea(MDCard):
    async def update_data(self, data, *args):
        self.ids.recycle_cont.data = []
        for mentor, group, subject, subject_type, hours in data:
            self.ids.recycle_cont.data.append(
                {
                    "viewclass": "ThreeLineListItem",
                    "text": f"Преподаватель: {mentor} | часов: {hours}.",
                    "secondary_text": f"Группа: {group}",
                    "tertiary_text": f"Предмет: {subject} ({subject_type})",
                }
            )
