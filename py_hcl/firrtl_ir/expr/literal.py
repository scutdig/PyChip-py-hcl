from ..type import UIntType, SIntType
from . import Expression
from ..utils import serialize_str


class UIntLiteral(Expression):
    def __init__(self, value, width):
        self.value = value
        self.tpe = UIntType(width)

    def serialize(self, output):
        self.tpe.serialize(output)
        output.write(b'("')
        output.write(serialize_str("h" + hex(self.value).replace("0x", "")))
        output.write(b'")')


class SIntLiteral(Expression):
    def __init__(self, value, width):
        self.value = value
        self.tpe = SIntType(width)

    def serialize(self, output):
        self.tpe.serialize(output)
        output.write(b'("')
        output.write(serialize_str("h" + hex(self.value).replace("0x", "")))
        output.write(b'")')
