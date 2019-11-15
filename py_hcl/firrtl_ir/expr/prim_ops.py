from .expression import Expression
from ..utils import serialize_num
from ..tpe import UIntType, SIntType, ClockType


def type_in(obj, *types):
    for t in types:
        if isinstance(obj, t):
            return True
    return False


def all_the_same(*objects):
    t = objects[0]
    for o in objects[1:]:
        if o != t:
            return False
    return True


def check_all_same_uint_sint(*types):
    for t in types:
        if not type_in(t, UIntType, SIntType):
            return False

    return all_the_same(*list(map(type, types)))


class Add(Expression):
    def __init__(self, args, tpe):
        self.args = args
        self.tpe = tpe

    def check_type(self):
        if not check_all_same_uint_sint(self.args[0].tpe,
                                        self.args[1].tpe,
                                        self.tpe):
            return False

        expected_type_width = max(self.args[0].tpe.width.width,
                                  self.args[1].tpe.width.width) + 1
        if self.tpe.width.width != expected_type_width:
            return False

        return True

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

    def check_type(self):
        if not check_all_same_uint_sint(self.args[0].tpe,
                                        self.args[1].tpe,
                                        self.tpe):
            return False

        expected_type_width = max(self.args[0].tpe.width.width,
                                  self.args[1].tpe.width.width) + 1
        if self.tpe.width.width != expected_type_width:
            return False

        return True

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

    def check_type(self):
        if not check_all_same_uint_sint(self.args[0].tpe,
                                        self.args[1].tpe,
                                        self.tpe):
            return False

        expected_type_width = \
            self.args[0].tpe.width.width + self.args[1].tpe.width.width
        if self.tpe.width.width != expected_type_width:
            return False

        return True

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

    def check_type(self):
        if not check_all_same_uint_sint(self.args[0].tpe,
                                        self.args[1].tpe,
                                        self.tpe):
            return False

        expected_type_width = self.args[0].tpe.width.width
        if type_in(self.args[0].tpe, SIntType):
            expected_type_width += 1
        if self.tpe.width.width != expected_type_width:
            return False

        return True

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

    def check_type(self):
        if not check_all_same_uint_sint(self.args[0].tpe,
                                        self.args[1].tpe,
                                        self.tpe):
            return False

        expected_type_width = min(self.args[0].tpe.width.width,
                                  self.args[1].tpe.width.width)
        if self.tpe.width.width != expected_type_width:
            return False

        return True

    def serialize(self, output):
        output.write(b"rem(")
        self.args[0].serialize(output)
        output.write(b", ")
        self.args[1].serialize(output)
        output.write(b")")


class _Comparison(Expression):
    def __init__(self, args, tpe):
        self.args = args
        self.tpe = tpe

    def check_type(self):
        if not check_all_same_uint_sint(self.args[0].tpe,
                                        self.args[1].tpe):
            return False

        if not type_in(self.tpe, UIntType):
            return False

        if self.tpe.width.width != 1:
            return False

        return True

    def serialize(self, output):
        output.write(b"(")
        self.args[0].serialize(output)
        output.write(b", ")
        self.args[1].serialize(output)
        output.write(b")")


class Lt(_Comparison):
    def serialize(self, output):
        output.write(b"lt")
        super().serialize(output)


class Leq(_Comparison):
    def serialize(self, output):
        output.write(b"leq")
        super().serialize(output)


class Gt(_Comparison):
    def serialize(self, output):
        output.write(b"gt")
        super().serialize(output)


class Geq(_Comparison):
    def serialize(self, output):
        output.write(b"geq")
        super().serialize(output)


class Eq(_Comparison):
    def serialize(self, output):
        output.write(b"eq")
        super().serialize(output)


class Neq(_Comparison):
    def serialize(self, output):
        output.write(b"neq")
        super().serialize(output)


class _BinaryBit(Expression):
    def __init__(self, args, tpe):
        self.args = args
        self.tpe = tpe

    def check_type(self):
        if not check_all_same_uint_sint(self.args[0].tpe,
                                        self.args[1].tpe,
                                        self.tpe):
            return False

        expected_type_width = max(self.args[0].tpe.width.width,
                                  self.args[1].tpe.width.width)
        if self.tpe.width.width != expected_type_width:
            return False

        return True

    def serialize(self, output):
        output.write(b"(")
        self.args[0].serialize(output)
        output.write(b", ")
        self.args[1].serialize(output)
        output.write(b")")


class And(_BinaryBit):
    def serialize(self, output):
        output.write(b"and")
        super().serialize(output)


class Or(_BinaryBit):
    def serialize(self, output):
        output.write(b"or")
        super().serialize(output)


class Xor(_BinaryBit):
    def serialize(self, output):
        output.write(b"xor")
        super().serialize(output)


class Not(Expression):
    def __init__(self, arg, tpe):
        self.arg = arg
        self.tpe = tpe

    def check_type(self):
        if not check_all_same_uint_sint(self.arg.tpe,
                                        self.tpe):
            return False

        expected_type_width = self.arg.tpe.width.width
        if self.tpe.width.width != expected_type_width:
            return False

        return True

    def serialize(self, output):
        output.write(b"not(")
        self.arg.serialize(output)
        output.write(b")")


class Neg(Expression):
    def __init__(self, arg, tpe):
        self.arg = arg
        self.tpe = tpe

    def check_type(self):
        if not check_all_same_uint_sint(self.arg.tpe,
                                        self.tpe):
            return False

        expected_type_width = self.arg.tpe.width.width + 1
        if self.tpe.width.width != expected_type_width:
            return False

        return True

    def serialize(self, output):
        output.write(b"neg(")
        self.arg.serialize(output)
        output.write(b")")


class Cat(Expression):
    def __init__(self, args, tpe):
        self.args = args
        self.tpe = tpe

    def check_type(self):
        if not check_all_same_uint_sint(self.args[0].tpe,
                                        self.args[1].tpe,
                                        self.tpe):
            return False

        expected_type_width = \
            self.args[0].tpe.width.width + self.args[1].tpe.width.width
        if self.tpe.width.width != expected_type_width:
            return False

        return True

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

    def check_type(self):
        if not check_all_same_uint_sint(self.ir_arg.tpe):
            return False

        if not type_in(self.tpe, UIntType):
            return False

        if not \
                self.tpe.width.width >= \
                self.const_args[0] >= \
                self.const_args[1] >= 0:
            return False

        expected_type_width = self.const_args[0] - self.const_args[1] + 1
        if self.tpe.width.width != expected_type_width:
            return False

        return True

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

    def check_type(self):
        if not type_in(self.arg.tpe, UIntType, SIntType, ClockType):
            return False

        if not type_in(self.tpe, UIntType):
            return False

        expected_type_width = self.arg.width.width
        if type_in(self.tpe, ClockType):
            expected_type_width = 1
        if self.tpe.width.width != expected_type_width:
            return False

        return True

    def serialize(self, output):
        output.write(b"asUInt(")
        self.arg.serialize(output)
        output.write(b")")


class AsSInt(Expression):
    def __init__(self, arg, tpe):
        self.arg = arg
        self.tpe = tpe

    def check_type(self):
        if not type_in(self.arg.tpe, UIntType, SIntType, ClockType):
            return False

        if not type_in(self.tpe, SIntType):
            return False

        expected_type_width = self.arg.width.width
        if type_in(self.tpe, ClockType):
            expected_type_width = 1
        if self.tpe.width.width != expected_type_width:
            return False

        return True

    def serialize(self, output):
        output.write(b"asSInt(")
        self.arg.serialize(output)
        output.write(b")")


class Shl(Expression):
    def __init__(self, ir_arg, const_arg, tpe):
        self.ir_arg = ir_arg
        self.const_arg = const_arg
        self.tpe = tpe

    def check_type(self):
        if not check_all_same_uint_sint(self.ir_arg.tpe, self.tpe):
            return False

        expected_type_width = self.ir_arg.width.width + self.const_arg
        if self.tpe.width.width != expected_type_width:
            return False

        return True

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

    def check_type(self):
        if not check_all_same_uint_sint(self.ir_arg.tpe, self.tpe):
            return False

        expected_type_width = self.ir_arg.width.width - self.const_arg
        expected_type_width = max(expected_type_width, 1)
        if self.tpe.width.width != expected_type_width:
            return False

        return True

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

    def check_type(self):
        if not check_all_same_uint_sint(self.args[0].tpe,
                                        self.tpe):
            return False

        if type_in(self.args[1].tpe, UIntType):
            return False

        expected_type_width = \
            self.args[0].width.width + 2 ** self.args[1].width.width - 1
        if self.tpe.width.width != expected_type_width:
            return False

        return True

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

    def check_type(self):
        if not check_all_same_uint_sint(self.args[0].tpe,
                                        self.tpe):
            return False

        if type_in(self.args[1].tpe, UIntType):
            return False

        expected_type_width = self.args[0].width.width
        if self.tpe.width.width != expected_type_width:
            return False

        return True

    def serialize(self, output):
        output.write(b"dshr(")
        self.args[0].serialize(output)
        output.write(b", ")
        self.args[1].serialize(output)
        output.write(b")")
