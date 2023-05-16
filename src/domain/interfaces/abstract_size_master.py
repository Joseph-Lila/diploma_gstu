class AbstractSizeMaster:
    def fit_slaves(self):
        raise NotImplementedError

    def expand_width(self, new_width):
        for slave in self.slaves:
            slave.set_width(new_width)

    def add_slaves(self, slaves):
        raise NotImplementedError
