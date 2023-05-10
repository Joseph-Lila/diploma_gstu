class AbstractSizeSlave:
    def get_minimum_width(self):
        raise NotImplementedError

    def set_width(self, width):
        self.size_hint_x = None
        self.width = width
