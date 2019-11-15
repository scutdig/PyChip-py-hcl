from .expression import Expression
from .utils import serialize_str


class UIntLiteral(Expression):
    def __init__(self, value, width):
        self.value = value
        self.width = width

    def serialize(self, output):
        output.write(b"UInt")
        self.width.serialize(output)
        output.write(b'("')
        output.write(serialize_str(hex(self.value)[2:]))
        output.write(b'")')


class SIntLiteral(Expression):
    def __init__(self, value, width):
        self.value = value
        self.width = width

    def serialize(self, output):
        output.write(b"SInt")
        self.width.serialize(output)
        output.write(b'("')
        output.write(serialize_str(hex(self.value)[2:]))
        output.write(b'")')
