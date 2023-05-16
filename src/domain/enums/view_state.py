import enum


class ViewState(enum.Enum):
    UNAVAILABLE = "UNAVAILABLE"
    EDITABLE = "EDITABLE"
    FILLED = "FILLED"
    INVISIBLE = "INVISIBLE"
    EMPTY = "EMPTY"
