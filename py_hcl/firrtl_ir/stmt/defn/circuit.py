from ...utils import serialize_str
from .. import Statement


class DefCircuit(Statement):
    def __init__(self, main, def_modules):
        self.main = main
        self.def_modules = def_modules

    def serialize_stmt(self, output, indent=0):
        output.write(b"circuit ")
        output.write(serialize_str(self.main))
        output.write(b" :\n")
        indent += 1
        for def_module in self.def_modules:
            output.write(serialize_str("  " * indent))
            def_module.serialize_stmt(output, indent)
            output.write(b"\n\n")
