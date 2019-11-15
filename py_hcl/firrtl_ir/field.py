"""
The field module provides information about the field
in BundleType.

Fields are allowed to be flipped, indicating that it's
opposite direction to the BundleType.

Each field includes
  name:        individual name of the field;
  type:        defined type;
  orientation: flipped or not.
"""
from .utils import serialize_str


class Field(object):
    def __init__(self, name, tpe, is_flipped=False):
        self.name = name
        self.tpe = tpe
        self.is_flipped = is_flipped

    def serialize(self, output):
        if self.is_flipped:
            output.write(b"flip ")
        output.write(serialize_str(self.name))
        output.write(b" : ")
        self.tpe.serialize(output)

    def field_eq(self, other):
        if type(other) != type(self):
            return False
        if self.name != other.name:
            return False
        if self.is_flipped != other.is_flipped:
            return False
        return self.tpe.type_eq(other.tpe)
