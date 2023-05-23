import enum


class ViewState(enum.Enum):
    UNAVAILABLE = "UNAVAILABLE"
    EDITABLE = "EDITABLE"
    FILLED = "FILLED"
    INVISIBLE = "INVISIBLE"
    EMPTY = "EMPTY"
    MENTOR_IS_BUSY = "MENTOR_IS_BUSY"
