class AbstractSizeMaster:
    def fit_slaves(self):
        if len(self.slaves) > 0:
            max_width = max(
                slave.get_minimum_width()
                for slave in self.slaves
            )
            for slave in self.slaves:
                slave.set_width(max_width)

    def expand_width(self, new_width):
        for slave in self.slaves:
            slave.set_width(new_width)
