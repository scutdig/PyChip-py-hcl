from ..utils import serialize_str
from . import Statement


class Block(Statement):
    def __init__(self, statements):
        self.statements = statements

    def serialize_stmt(self, output, indent):
        for stmt in self.statements[:-1]:
            stmt.serialize_stmt(output, indent)
            output.write(b"\n")
            output.write(serialize_str("  " * indent))
        self.statements[-1].serialize_stmt(output, indent)
