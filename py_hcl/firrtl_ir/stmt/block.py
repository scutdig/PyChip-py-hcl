from . import Statement


class Block(Statement):
    def __init__(self, statements):
        self.statements = statements

    def serialize(self, output):
        for stmt in self.statements[:-1]:
            stmt.serialize(output)
            output.write(b"\n")
        self.statements[-1].serialize(output)
