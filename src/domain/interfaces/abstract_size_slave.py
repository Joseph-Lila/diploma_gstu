class AbstractSizeSlave:
    def get_minimum_width(self):
        raise NotImplementedError

    def set_width(self, width):
        raise NotImplementedError

    def set_invisible_width(self):
        raise NotImplementedError
