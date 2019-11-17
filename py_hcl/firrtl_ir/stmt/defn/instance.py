from ...utils import serialize_str
from .. import Statement


class DefInstance(Statement):
    def __init__(self, name, module_name):
        self.name = name
        self.module_name = module_name

    def serialize_stmt(self, output, indent):
        output.write(b"inst ")
        output.write(serialize_str(self.name))
        output.write(b" of ")
        output.write(serialize_str(self.module_name))
