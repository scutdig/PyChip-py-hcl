from ...utils import serialize_str
from .. import Statement


class DefNode(Statement):
    def __init__(self, name, expr_ref):
        self.name = name
        self.expr_ref = expr_ref

    def serialize_stmt(self, output, indent):
        output.write(b"node ")
        output.write(serialize_str(self.name))
        output.write(b" = ")
        self.expr_ref.serialize(output)
