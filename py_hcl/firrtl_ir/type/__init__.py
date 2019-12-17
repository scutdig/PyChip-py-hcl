from ..utils import serialize_num


class UnknownType(object):
    def serialize(self, output):
        output.write(b"?")


class GroundType(object):
    pass


class UIntType(GroundType):
    def __init__(self, width):
        self.width = width

    def serialize(self, output):
        output.write(b"UInt")
        self.width.serialize(output)


class SIntType(GroundType):
    def __init__(self, width):
        self.width = width

    def serialize(self, output):
        output.write(b"SInt")
        self.width.serialize(output)


class ClockType(GroundType):
    def serialize(self, output):
        output.write(b"Clock")


class AggregateType(object):
    pass


class BundleType(AggregateType):
    def __init__(self, fields):
        self.fields = fields

    def serialize(self, output):
        output.write(b"{")
        for f in self.fields[:-1]:
            f.serialize(output)
            output.write(b", ")
        self.fields[-1].serialize(output)
        output.write(b"}")


class VectorType(AggregateType):
    def __init__(self, elem_type, size):
        self.elem_type = elem_type
        self.size = size

    def serialize(self, output):
        self.elem_type.serialize(output)
        output.write(b"[")
        output.write(serialize_num(self.size))
        output.write(b"]")
