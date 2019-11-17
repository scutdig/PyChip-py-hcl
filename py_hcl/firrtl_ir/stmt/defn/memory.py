from ...utils import serialize_str
from .. import Statement


class DefMemory(Statement):
    def __init__(self, name, tpe):
        self.name = name
        self.tpe = tpe

    def serialize_stmt(self, output, indent):
        output.write(b"cmem ")
        output.write(serialize_str(self.name))
        output.write(b" : ")
        self.tpe.serialize(output)


class DefMemReadPort(Statement):
    def __init__(self, name, mem_ref, index_ref, clock_ref):
        self.name = name
        self.mem_ref = mem_ref
        self.index_ref = index_ref
        self.clock_ref = clock_ref

    def serialize_stmt(self, output, indent):
        output.write(b"read mport ")
        output.write(serialize_str(self.name))
        output.write(b" = ")
        self.mem_ref.serialize(output)
        output.write(b"[")
        self.index_ref.serialize(output)
        output.write(b"], ")
        self.clock_ref.serialize(output)


class DefMemWritePort(Statement):
    def __init__(self, name, mem_ref, index_ref, clock_ref):
        self.name = name
        self.mem_ref = mem_ref
        self.index_ref = index_ref
        self.clock_ref = clock_ref

    def serialize_stmt(self, output, indent):
        output.write(b"write mport ")
        output.write(serialize_str(self.name))
        output.write(b" = ")
        self.mem_ref.serialize(output)
        output.write(b"[")
        self.index_ref.serialize(output)
        output.write(b"], ")
        self.clock_ref.serialize(output)
