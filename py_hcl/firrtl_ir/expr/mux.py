from . import Expression


class Mux(Expression):
    def __init__(self, cond, tval, fval, tpe):
        self.cond = cond
        self.tval = tval
        self.fval = fval
        self.tpe = tpe

    def serialize(self, output):
        output.write(b"mux(")
        self.cond.serialize(output)
        output.write(b", ")
        self.tval.serialize(output)
        output.write(b", ")
        self.fval.serialize(output)
        output.write(b")")
