from .utils import serialize_num, serialize_str
from .expression import Expression


class PrimCall(Expression):
    def __init__(self, prim_op, ir_args, const_args, tpe):
        self.prim_op = prim_op
        self.ir_args = ir_args
        self.const_args = const_args
        self.tpe = tpe

    def serialize(self, output):
        output.write(serialize_str(self.prim_op))
        output.write(b"(")

        comma_cnt = len(self.ir_args) + len(self.const_args) - 1

        for ir_arg in self.ir_args:
            ir_arg.serialize(output)
            if comma_cnt > 0:
                comma_cnt -= 1
                output.write(b", ")

        for const_arg in self.const_args:
            output.write(serialize_num(const_arg))
            if comma_cnt > 0:
                comma_cnt -= 1
                output.write(b", ")

        output.write(b")")
