"""
The tpe module provides type nodes in FIRRTL IR.

At the top level of types include UnknownType, GroundType, AggregateType.
GroundType acts as a primitive type, and AggregateType is similar to a
data structure composed of GroundType.

GroundType includes
  UIntType:  unsigned integer;
  SIntType:  signed integer;
  ClockType: represents the clock.

AggregateType includes BundleType, similar to the structs in high-level
languages, composed of various fields of different types. VectorType
is similar to arrays in high-level languages, holds multiple elements of
the same type.
"""
from .utils import serialize_num


class UnknownType(object):
    def serialize(self, output):
        output.write(b"?")

    def type_eq(self, other):
        if type(other) != type(self):
            return False
        return True


class GroundType(object):
    pass


class UIntType(GroundType):
    def __init__(self, width):
        self.width = width

    def serialize(self, output):
        output.write(b"UInt")
        self.width.serialize(output)

    def type_eq(self, other):
        if type(other) != type(self):
            return False
        return self.width.width_eq(other.width)


class SIntType(GroundType):
    def __init__(self, width):
        self.width = width

    def serialize(self, output):
        output.write(b"SInt")
        self.width.serialize(output)

    def type_eq(self, other):
        if type(other) != type(self):
            return False
        return self.width.width_eq(other.width)


class ClockType(GroundType):
    def serialize(self, output):
        output.write(b"Clock")

    def type_eq(self, other):
        if type(other) != type(self):
            return False
        return True


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

    def type_eq(self, other):
        if type(other) != type(self):
            return False
        for (a, b) in zip(self.fields, other.fields):
            if not a.field_eq(b):
                return False
        return True


class VectorType(AggregateType):
    def __init__(self, elem_type, size):
        self.elem_type = elem_type
        self.size = size

    def serialize(self, output):
        self.elem_type.serialize(output)
        output.write(b"[")
        output.write(serialize_num(self.size))
        output.write(b"]")

    def type_eq(self, other):
        if type(other) != type(self):
            return False
        if not self.elem_type.type_eq(other.elem_type):
            return False
        if self.size != other.size:
            return False
        return True
