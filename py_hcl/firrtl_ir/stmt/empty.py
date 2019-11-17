from . import Statement


class EmptyStmt(Statement):
    def serialize_stmt(self, output, indent):
        output.write(b"skip")
