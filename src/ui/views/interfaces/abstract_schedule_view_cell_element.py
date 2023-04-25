from src.adapters.orm import ScheduleRecord


class AbstractScheduleViewCellElement:
    """
    This class represents ScheduleRecord entity.
    But instead of xxx_id here we use Extended Dataclasses.
    """
    def set_schedule_record(self, *args):
        raise NotImplementedError

    def get_schedule_record(self, *args) -> ScheduleRecord:
        raise NotImplementedError

    def send_command_to_check_if_cell_can_be_filled(self, *args):
        """
        Method to send command after clicking on option 'Edit' in the dropdown menu.
        It is needed to prevent waste of user time.
        We need to check if user have at least one combination of parameters to fill current cell.

        :param args:
        :return: None
        """
        raise NotImplementedError

    def open_editing_dialog_or_show_alert_dialog(self, conclusion: bool):
        """
        Method to process message came due to 'send_command_to_check_if_cell_can_be_filled'.
        If user will be able to fill the cell with at least one combination,
        conclusion will be set to 'True' and we show filling dialog.
        Else we need to notify user about the situation.

        :param conclusion: bool
        :return: None
        """
        raise NotImplementedError
