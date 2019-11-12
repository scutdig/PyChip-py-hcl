"""
The tpe module provides bit width information for UIntType
and SIntType.

"""

from .utils import serialize_num


class Width(object):
    pass


class IntWidth(Width):
    def __init__(self, width):
        self.width = width

    def serialize(self, output):
        output.write(b"<")
        output.write(serialize_num(self.width))
        output.write(b">")


class UnknownWidth(Width):
    def serialize(self, output):
        pass
