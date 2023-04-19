from kivy.app import App
from kivy.uix.modalview import ModalView
from kivymd.uix.card import MDCard
import asynckivy as ak
from kivy.core.audio import SoundLoader
import csv


class WorkloadsManagerDialog(MDCard, ModalView):
    mentor_hint = "Преподаватель"
    group_hint = "Группа"
    subject_hint = "Предмет"
    subject_type_hint = "Тип предмета"
    hour_hint = "Часы"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sound = SoundLoader.load("assets/music/notification.mp3")
        self.mentors = set()
        self.groups = set()
        self.subjects = set()
        self.hours = set()
        self.subject_types = ["Лекция", "Лабораторная"]

    async def fill_mentors_selector(self, selector, text):
        await selector.update_variants(
            sorted([r for r in self.mentors if text.lower() in r.lower()])
        )

    async def fill_hours_selector(self, selector, text):
        await selector.update_variants(
            sorted([r for r in self.hours if text.lower() in r.lower()])
        )

    async def fill_subject_types_selector(self, selector, text):
        await selector.update_variants(
            sorted([r for r in self.subject_types if text.lower() in r.lower()])
        )

    async def fill_subjects_selector(self, selector, text):
        await selector.update_variants(
            sorted([r for r in self.subjects if text.lower() in r.lower()])
        )

    async def fill_groups_selector(self, selector, text):
        await selector.update_variants(
            sorted([r for r in self.groups if text.lower() in r.lower()])
        )

    def open(self, *args, **kwargs):
        super().open(*args, **kwargs)

    def send_command_to_get_mentors_fios(self, *args):
        ak.start(
            self.fill_mentors_selector(
                self.ids.mentor,
                self.ids.mentor.text,
            )
        )

    def send_command_to_get_hours(self, *args):
        ak.start(
            self.fill_hours_selector(
                self.ids.hour,
                self.ids.hour.text,
            )
        )

    def send_command_to_get_subjects(self, *args):
        ak.start(
            self.fill_subjects_selector(
                self.ids.subject,
                self.ids.subject.text,
            )
        )

    def send_command_to_get_subject_types(self, *args):
        ak.start(
            self.fill_subject_types_selector(
                self.ids.subject_type,
                self.ids.subject_type.text,
            )
        )

    def send_command_to_get_groups_titles(self, *args):
        ak.start(
            self.fill_groups_selector(
                self.ids.group,
                self.ids.group.text,
            )
        )

    def add_record(self, *args):
        self.ids.add_btn.disabled = True
        if self.ids.mentor.text:
            self.mentors.add(self.ids.mentor.text)
        if self.ids.group.text:
            self.groups.add(self.ids.group.text)
        if self.ids.subject.text:
            self.subjects.add(self.ids.subject.text)
        if self.ids.hour.text:
            self.hours.add(self.ids.hour.text)
        fields = [
            self.ids.mentor.text,
            self.ids.group.text,
            self.ids.subject.text,
            self.ids.subject_type.text,
            self.ids.hour.text,
        ]
        if all(fields):
            if self.sound:
                self.sound.play()
            with open("assets/csv/all.csv", "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(fields)
        self.ids.add_btn.disabled = False
