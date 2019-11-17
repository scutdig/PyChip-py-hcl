from . import Statement


class Connect(Statement):
    def __init__(self, loc_ref, expr_ref):
        self.loc_ref = loc_ref
        self.expr_ref = expr_ref

    def serialize_stmt(self, output, indent):
        self.loc_ref.serialize(output)
        output.write(b" <= ")
        self.expr_ref.serialize(output)
