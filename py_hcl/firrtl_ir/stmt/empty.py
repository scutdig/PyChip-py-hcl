from . import Statement


class EmptyStmt(Statement):
    def serialize(self, output):
        output.write(b"skip")
