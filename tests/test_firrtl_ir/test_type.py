from py_hcl.firrtl_ir import tpe, width, field
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


def test_bundle_type():
    bd = tpe.BundleType([
        field.Field("a", tpe.UIntType(width.IntWidth(8))),
        field.Field("b", tpe.UIntType(width.IntWidth(8))),
        field.Field("c", tpe.UIntType(width.IntWidth(8)), True),
    ])
    serialize_equal(bd, "{a : UInt<8>, b : UInt<8>, flip c : UInt<8>}")

    vt = tpe.VectorType(tpe.UIntType(width.IntWidth(8)), 16)
    bd = tpe.BundleType([
        field.Field("a", vt),
        field.Field("b", tpe.UIntType(width.IntWidth(8)), True),
        field.Field("c", tpe.VectorType(vt, 32)),
    ])
    serialize_equal(
        bd, "{a : UInt<8>[16], flip b : UInt<8>, c : UInt<8>[16][32]}"
    )

    # TODO: Is it valid?
    bd = tpe.BundleType([
        field.Field("l1", tpe.BundleType([
            field.Field("l2", tpe.BundleType([
                field.Field("l3", tpe.UIntType(width.IntWidth(8)), True)
            ])),
            field.Field("vt", vt),
        ]))
    ])
    serialize_equal(bd, "{l1 : {l2 : {flip l3 : UInt<8>}, vt : UInt<8>[16]}}")
