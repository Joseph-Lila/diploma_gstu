class AbstractSizeSlave:
    def get_minimum_width(self):
        raise NotImplementedError

    def set_width(self, width):
        self.size_hint_x = None
        self.size_hint_y = 1
        self.width = width

    def set_invisible_width(self):
        raise NotImplementedError
