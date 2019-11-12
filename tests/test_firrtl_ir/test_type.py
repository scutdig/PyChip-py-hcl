from py_hcl.firrtl_ir import tpe, width
from .utils import serialize_equal


def test_unknown_type():
    serialize_equal(tpe.UnknownType(), "?")


def test_clock_type():
    serialize_equal(tpe.ClockType(), "Clock")


def test_uint_type():
    serialize_equal(tpe.UIntType(width.UnknownWidth()), "UInt")
    serialize_equal(tpe.UIntType(width.IntWidth(8)), "UInt<8>")
    serialize_equal(tpe.UIntType(width.IntWidth(32)), "UInt<32>")


def test_sint_type():
    serialize_equal(tpe.SIntType(width.UnknownWidth()), "SInt")
    serialize_equal(tpe.SIntType(width.IntWidth(8)), "SInt<8>")
    serialize_equal(tpe.SIntType(width.IntWidth(32)), "SInt<32>")


def test_vector_type():
    vt = tpe.VectorType(tpe.UIntType(width.UnknownWidth()), 16)
    serialize_equal(vt, "UInt[16]")

    vt = tpe.VectorType(tpe.SIntType(width.IntWidth(8)), 16)
    serialize_equal(vt, "SInt<8>[16]")

    vt = tpe.VectorType(tpe.UIntType(width.IntWidth(8)), 16)
    serialize_equal(vt, "UInt<8>[16]")

    vt = tpe.VectorType(vt, 32)
    serialize_equal(vt, "UInt<8>[16][32]")

    vt = tpe.VectorType(tpe.VectorType(tpe.VectorType(vt, 42), 7), 9)
    serialize_equal(vt, "UInt<8>[16][32][42][7][9]")
