from src.domain.commands import GetExtendedScheduleRecords
from src.ui.controller import use_loop


class ScheduleMaster:
    def __init__(self, model):
        self._model = model
        self._schedule_id = None
        self._year = None
        self._term = None
        self._observers = []
        self._half_elements = []  # to control half elements

    @property
    def id(self):
        return self._schedule_id

    @property
    def year(self):
        return self._year

    @property
    def term(self):
        return self._term

    @use_loop
    async def update_metadata(
            self,
            id_,
            year,
            term,
    ):
        self._schedule_id = id_
        self._year = year
        self._term = term
        df = await self._model.bus.handle_command(GetExtendedScheduleRecords(id_))
        print(df)

    def register_observer(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self, *args):
        pass

    def consider_the_proposal(self, *args, check_presented_observers=False):
        pass

    def give_data_variants_for_observer(self, *args):
        pass
