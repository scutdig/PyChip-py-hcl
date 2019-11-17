from . import Expression
from ..utils import serialize_num


class Add(Expression):
    def __init__(self, args, tpe):
        self.args = args
        self.tpe = tpe

    def serialize(self, output):
        output.write(b"add(")
        self.args[0].serialize(output)
        output.write(b", ")
        self.args[1].serialize(output)
        output.write(b")")


class Sub(Expression):
    def __init__(self, args, tpe):
        self.args = args
        self.tpe = tpe

    def serialize(self, output):
        output.write(b"sub(")
        self.args[0].serialize(output)
        output.write(b", ")
        self.args[1].serialize(output)
        output.write(b")")


class Mul(Expression):
    def __init__(self, args, tpe):
        self.args = args
        self.tpe = tpe

    def serialize(self, output):
        output.write(b"mul(")
        self.args[0].serialize(output)
        output.write(b", ")
        self.args[1].serialize(output)
        output.write(b")")


class Div(Expression):
    def __init__(self, args, tpe):
        self.args = args
        self.tpe = tpe

    def serialize(self, output):
        output.write(b"div(")
        self.args[0].serialize(output)
        output.write(b", ")
        self.args[1].serialize(output)
        output.write(b")")


class Rem(Expression):
    def __init__(self, args, tpe):
        self.args = args
        self.tpe = tpe

    def serialize(self, output):
        output.write(b"rem(")
        self.args[0].serialize(output)
        output.write(b", ")
        self.args[1].serialize(output)
        output.write(b")")


class Lt(Expression):
    def __init__(self, args, tpe):
        self.args = args
        self.tpe = tpe

    def serialize(self, output):
        output.write(b"lt(")
        self.args[0].serialize(output)
        output.write(b", ")
        self.args[1].serialize(output)
        output.write(b")")


class Leq(Expression):
    def __init__(self, args, tpe):
        self.args = args
        self.tpe = tpe

    def serialize(self, output):
        output.write(b"leq(")
        self.args[0].serialize(output)
        output.write(b", ")
        self.args[1].serialize(output)
        output.write(b")")


class Gt(Expression):
    def __init__(self, args, tpe):
        self.args = args
        self.tpe = tpe

    def serialize(self, output):
        output.write(b"gt(")
        self.args[0].serialize(output)
        output.write(b", ")
        self.args[1].serialize(output)
        output.write(b")")


class Geq(Expression):
    def __init__(self, args, tpe):
        self.args = args
        self.tpe = tpe

    def serialize(self, output):
        output.write(b"geq(")
        self.args[0].serialize(output)
        output.write(b", ")
        self.args[1].serialize(output)
        output.write(b")")


class Eq(Expression):
    def __init__(self, args, tpe):
        self.args = args
        self.tpe = tpe

    def serialize(self, output):
        output.write(b"eq(")
        self.args[0].serialize(output)
        output.write(b", ")
        self.args[1].serialize(output)
        output.write(b")")


class Neq(Expression):
    def __init__(self, args, tpe):
        self.args = args
        self.tpe = tpe

    def serialize(self, output):
        output.write(b"neq(")
        self.args[0].serialize(output)
        output.write(b", ")
        self.args[1].serialize(output)
        output.write(b")")


class And(Expression):
    def __init__(self, args, tpe):
        self.args = args
        self.tpe = tpe

    def serialize(self, output):
        output.write(b"and(")
        self.args[0].serialize(output)
        output.write(b", ")
        self.args[1].serialize(output)
        output.write(b")")


class Or(Expression):
    def __init__(self, args, tpe):
        self.args = args
        self.tpe = tpe

    def serialize(self, output):
        output.write(b"or(")
        self.args[0].serialize(output)
        output.write(b", ")
        self.args[1].serialize(output)
        output.write(b")")


class Xor(Expression):
    def __init__(self, args, tpe):
        self.args = args
        self.tpe = tpe

    def serialize(self, output):
        output.write(b"xor(")
        self.args[0].serialize(output)
        output.write(b", ")
        self.args[1].serialize(output)
        output.write(b")")


class Not(Expression):
    def __init__(self, arg, tpe):
        self.arg = arg
        self.tpe = tpe

    def serialize(self, output):
        output.write(b"not(")
        self.arg.serialize(output)
        output.write(b")")


class Neg(Expression):
    def __init__(self, arg, tpe):
        self.arg = arg
        self.tpe = tpe

    def serialize(self, output):
        output.write(b"neg(")
        self.arg.serialize(output)
        output.write(b")")


class Cat(Expression):
    def __init__(self, args, tpe):
        self.args = args
        self.tpe = tpe

    def serialize(self, output):
        output.write(b"cat(")
        self.args[0].serialize(output)
        output.write(b", ")
        self.args[1].serialize(output)
        output.write(b")")


class Bits(Expression):
    def __init__(self, ir_arg, const_args, tpe):
        self.ir_arg = ir_arg
        self.const_args = const_args
        self.tpe = tpe

    def serialize(self, output):
        output.write(b"bits(")
        self.ir_arg.serialize(output)
        output.write(b", ")
        output.write(serialize_num(self.const_args[0]))
        output.write(b", ")
        output.write(serialize_num(self.const_args[1]))
        output.write(b")")


class AsUInt(Expression):
    def __init__(self, arg, tpe):
        self.arg = arg
        self.tpe = tpe

    def serialize(self, output):
        output.write(b"asUInt(")
        self.arg.serialize(output)
        output.write(b")")


class AsSInt(Expression):
    def __init__(self, arg, tpe):
        self.arg = arg
        self.tpe = tpe

    def serialize(self, output):
        output.write(b"asSInt(")
        self.arg.serialize(output)
        output.write(b")")


class Shl(Expression):
    def __init__(self, ir_arg, const_arg, tpe):
        self.ir_arg = ir_arg
        self.const_arg = const_arg
        self.tpe = tpe

    def serialize(self, output):
        output.write(b"shl(")
        self.ir_arg.serialize(output)
        output.write(b", ")
        output.write(serialize_num(self.const_arg))
        output.write(b")")


class Shr(Expression):
    def __init__(self, ir_arg, const_arg, tpe):
        self.ir_arg = ir_arg
        self.const_arg = const_arg
        self.tpe = tpe

    def serialize(self, output):
        output.write(b"shr(")
        self.ir_arg.serialize(output)
        output.write(b", ")
        output.write(serialize_num(self.const_arg))
        output.write(b")")


class Dshl(Expression):
    def __init__(self, args, tpe):
        self.args = args
        self.tpe = tpe

    def serialize(self, output):
        output.write(b"dshl(")
        self.args[0].serialize(output)
        output.write(b", ")
        self.args[1].serialize(output)
        output.write(b")")


class Dshr(Expression):
    def __init__(self, args, tpe):
        self.args = args
        self.tpe = tpe

    def serialize(self, output):
        output.write(b"dshr(")
        self.args[0].serialize(output)
        output.write(b", ")
        self.args[1].serialize(output)
        output.write(b")")
