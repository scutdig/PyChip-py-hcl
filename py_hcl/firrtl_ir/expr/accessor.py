from ..utils import serialize_str, serialize_num
from . import Expression


class SubField(Expression):
    def __init__(self, bundle_ref, name, tpe):
        self.bundle_ref = bundle_ref
        self.name = name
        self.tpe = tpe

    def serialize(self, output):
        self.bundle_ref.serialize(output)
        output.write(b".")
        output.write(serialize_str(self.name))


class SubIndex(Expression):
    def __init__(self, vector_ref, index, tpe):
        self.vector_ref = vector_ref
        self.index = index
        self.tpe = tpe

    def serialize(self, output):
        self.vector_ref.serialize(output)
        output.write(b"[")
        output.write(serialize_num(self.index))
        output.write(b"]")


class SubAccess(Expression):
    def __init__(self, vector_ref, index_ref, tpe):
        self.vector_ref = vector_ref
        self.index_ref = index_ref
        self.tpe = tpe

    def serialize(self, output):
        self.vector_ref.serialize(output)
        output.write(b"[")
        self.index_ref.serialize(output)
        output.write(b"]")
