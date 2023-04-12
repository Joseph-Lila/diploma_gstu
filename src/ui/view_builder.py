from src.ui.controller import Controller


class ViewBuilder:
    def __init__(self, controller: Controller):
        self.controller: Controller = controller

    def generate_main_view(
            self,
    ):
        """
        Only this method must be synchronous
        because it calls one time and in the beginning.
        :return:
        """
        # main_view.view_builder = self
        raise NotImplementedError
