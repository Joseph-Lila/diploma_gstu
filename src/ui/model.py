from typing import Optional
from dataclasses import dataclass

from src.service_layer.messagebus import MessageBus
from src.ui.schedule_master import ScheduleMaster


@dataclass
class Model:
    bus: Optional[MessageBus]
    schedule_master: Optional[ScheduleMaster]

    def create_schedule_master(self):
        self.schedule_master = ScheduleMaster(self)
