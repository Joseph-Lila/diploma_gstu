from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.expansionpanel import MDExpansionPanelOneLine, MDExpansionPanel, MDExpansionPanelThreeLine
from kivymd.uix.list import ThreeLineListItem


class WorkloadArea(MDCard):
    async def update_data(self, data, *args):
        self.ids.box.clear_widgets()
        mentor_expansion_panels = {}
        for mentor, group, subject, subject_type, hours in data:
            if mentor not in mentor_expansion_panels:
                mentor_expansion_panels[mentor] = MDExpansionPanel(
                    icon='human-male-board',
                    content=MDBoxLayout(
                        adaptive_height=True,
                        orientation='vertical',
                    ),
                    panel_cls=MDExpansionPanelOneLine(
                        text=mentor,
                    )
                )
            mentor_expansion_panels[mentor].content.add_widget(
                ThreeLineListItem(
                    text=f"Группа: {group}",
                    secondary_text=f"Занятие: {subject} ({subject_type})",
                    tertiary_text=f"Число часов: {hours}",
                )
            )
        for key, value in mentor_expansion_panels.items():
            self.ids.box.add_widget(value)
