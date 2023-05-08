from dataclasses import dataclass
from typing import List

from pandas import DataFrame

from src.adapters.orm import Schedule
from src.domain.events.event import Event


@dataclass
class GotDataFrame(Event):
    df: DataFrame
