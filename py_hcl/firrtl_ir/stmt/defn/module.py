from ...utils import serialize_str
from .. import Statement


class InputPort(object):
    def __init__(self, name, tpe):
        self.name = name
        self.tpe = tpe

    def serialize(self, output):
        output.write(b"input ")
        output.write(serialize_str(self.name))
        output.write(b" : ")
        self.tpe.serialize(output)


class OutputPort(object):
    def __init__(self, name, tpe):
        self.name = name
        self.tpe = tpe

    def serialize(self, output):
        output.write(b"output ")
        output.write(serialize_str(self.name))
        output.write(b" : ")
        self.tpe.serialize(output)


class DefModule(Statement):
    def __init__(self, name, ports, body):
        self.name = name
        self.ports = ports
        self.body = body

    def serialize_stmt(self, output, indent):
        output.write(b"module ")
        output.write(serialize_str(self.name))
        output.write(b" :\n")
        indent += 1
        for port in self.ports:
            output.write(serialize_str("  " * indent))
            port.serialize(output)
            output.write(b"\n")
        output.write(b"\n")
        output.write(serialize_str("  " * indent))
        self.body.serialize_stmt(output, indent)


class DefExtModule(Statement):
    def __init__(self, name, ports, def_name):
        self.name = name
        self.ports = ports
        self.def_name = def_name

    def serialize_stmt(self, output, indent):
        output.write(b"extmodule ")
        output.write(serialize_str(self.name))
        output.write(b" :\n")
        indent += 1
        for port in self.ports:
            output.write(serialize_str("  " * indent))
            port.serialize(output)
            output.write(b"\n")
        output.write(b"\n")
        output.write(serialize_str("  " * indent))
        output.write(b"defname = ")
        output.write(serialize_str(self.def_name))
