class ScheduleMaster:
    def __init__(self):
        self._id = None
        self._year = None
        self._term = None

    @property
    def id(self):
        return self._id

    @property
    def year(self):
        return self._year

    @property
    def term(self):
        return self._term

    def update_metadata(
            self,
            id_,
            year,
            term,
    ):
        self._id = id_
        self._year = year
        self._term = term
