from py_hcl.firrtl_ir.expr.literal import SIntLiteral, UIntLiteral
from py_hcl.firrtl_ir.width import Width
from .utils import serialize_equal


def test_sint_literal():
    serialize_equal(SIntLiteral(10, Width(5)), 'SInt<5>("a")')
    serialize_equal(SIntLiteral(1023, Width(10)), 'SInt<10>("3ff")')


def test_uint_literal():
    serialize_equal(UIntLiteral(10, Width(5)), 'UInt<5>("a")')
    serialize_equal(UIntLiteral(1023, Width(10)), 'UInt<10>("3ff")')
