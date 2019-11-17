from ...utils import serialize_str
from .. import Statement


class DefRegister(Statement):
    def __init__(self, name, tpe, clock_ref):
        self.name = name
        self.tpe = tpe
        self.clock_ref = clock_ref

    def serialize_stmt(self, output, indent):
        output.write(b"reg ")
        output.write(serialize_str(self.name))
        output.write(b" : ")
        self.tpe.serialize(output)
        output.write(b", ")
        self.clock_ref.serialize(output)


class DefInitRegister(Statement):
    def __init__(self, name, tpe, clock_ref, reset_ref, init_ref):
        self.name = name
        self.tpe = tpe
        self.clock_ref = clock_ref
        self.reset_ref = reset_ref
        self.init_ref = init_ref

    def serialize_stmt(self, output, indent):
        output.write(b"reg ")
        output.write(serialize_str(self.name))
        output.write(b" : ")
        self.tpe.serialize(output)
        output.write(b", ")
        self.clock_ref.serialize(output)
        output.write(b" with :\n")
        output.write(serialize_str("  " * (indent + 1)))
        output.write(b"reset => (")
        self.reset_ref.serialize(output)
        output.write(b", ")
        self.init_ref.serialize(output)
        output.write(b")")
