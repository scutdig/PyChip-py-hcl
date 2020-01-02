from py_hcl.core.type import HclType


class ClockT(HclType):
    def __init__(self):
        self.type = "clock"
