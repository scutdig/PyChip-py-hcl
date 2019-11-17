from ...utils import serialize_str
from .. import Statement


class DefWire(Statement):
    def __init__(self, name, tpe):
        self.name = name
        self.tpe = tpe

    def serialize(self, output):
        output.write(b"wire ")
        output.write(serialize_str(self.name))
        output.write(b" : ")
        self.tpe.serialize(output)
