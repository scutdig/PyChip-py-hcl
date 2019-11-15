from py_hcl.firrtl_ir.literal import SIntLiteral, UIntLiteral
from py_hcl.firrtl_ir.width import IntWidth, UnknownWidth
from .utils import serialize_equal


def test_sint_literal():
    serialize_equal(SIntLiteral(10, IntWidth(5)), 'SInt<5>("a")')
    serialize_equal(SIntLiteral(10, UnknownWidth()), 'SInt("a")')
    serialize_equal(SIntLiteral(1023, IntWidth(10)), 'SInt<10>("3ff")')


def test_uint_literal():
    serialize_equal(UIntLiteral(10, IntWidth(5)), 'UInt<5>("a")')
    serialize_equal(UIntLiteral(10, UnknownWidth()), 'UInt("a")')
    serialize_equal(UIntLiteral(1023, IntWidth(10)), 'UInt<10>("3ff")')
