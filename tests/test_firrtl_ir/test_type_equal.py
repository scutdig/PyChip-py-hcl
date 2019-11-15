from py_hcl.firrtl_ir.field import Field
from py_hcl.firrtl_ir.tpe import UnknownType, ClockType, \
    UIntType, SIntType, VectorType, BundleType
from py_hcl.firrtl_ir.width import Width


def test_type_eq():
    assert UnknownType().type_eq(
        UnknownType()
    )
    assert ClockType().type_eq(
        ClockType()
    )
    assert UIntType(Width(10)).type_eq(
        UIntType(Width(10))
    )
    assert SIntType(Width(10)).type_eq(
        SIntType(Width(10))
    )
    assert VectorType(UIntType(Width(10)), 8).type_eq(
        VectorType(UIntType(Width(10)), 8)
    )
    assert BundleType([
        Field("a", VectorType(UIntType(Width(10)), 8)),
        Field("b", UIntType(Width(10)))
    ]).type_eq(
        BundleType([
            Field("a", VectorType(UIntType(Width(10)), 8)),
            Field("b", UIntType(Width(10)))
        ])
    )


def test_type_neq():
    assert not UnknownType().type_eq(
        ClockType()
    )
    assert not UnknownType().type_eq(UIntType(
        Width(10))
    )
    assert not UnknownType().type_eq(SIntType(
        Width(10))
    )
    assert not UnknownType().type_eq(VectorType(
        UIntType(Width(10)), 8)
    )
    assert not UnknownType().type_eq(VectorType(
        SIntType(Width(10)), 8)
    )
    assert not UnknownType().type_eq(
        BundleType([
            Field("a", VectorType(UIntType(Width(10)), 8)),
            Field("b", UIntType(Width(10)))
        ])
    )

    assert not ClockType().type_eq(
        UIntType(Width(10))
    )
    assert not ClockType().type_eq(
        SIntType(Width(10))
    )
    assert not ClockType().type_eq(
        VectorType(UIntType(Width(10)), 8)

    )
    assert not ClockType().type_eq(
        VectorType(SIntType(Width(10)), 8)
    )
    assert not ClockType().type_eq(
        BundleType([
            Field("a", VectorType(UIntType(Width(10)), 8)),
            Field("b", UIntType(Width(10)))
        ])
    )

    assert not UIntType(Width(10)).type_eq(
        UIntType(Width(8))
    )
    assert not UIntType(Width(10)).type_eq(
        SIntType(Width(10))
    )
    assert not UIntType(Width(10)).type_eq(
        VectorType(UIntType(Width(10)), 8)
    )
    assert not UIntType(Width(10)).type_eq(
        VectorType(SIntType(Width(10)), 8)
    )
    assert not UIntType(Width(10)).type_eq(
        BundleType([
            Field("a", VectorType(UIntType(Width(10)), 8)),
            Field("b", UIntType(Width(10)))
        ])
    )

    assert not SIntType(Width(10)).type_eq(
        SIntType(Width(8))
    )
    assert not SIntType(Width(10)).type_eq(
        VectorType(UIntType(Width(10)), 8)
    )
    assert not SIntType(Width(10)).type_eq(
        VectorType(SIntType(Width(10)), 8)
    )
    assert not SIntType(Width(10)).type_eq(
        BundleType([
            Field("a", VectorType(UIntType(Width(10)), 8)),
            Field("b", UIntType(Width(10)))
        ])
    )

    assert not VectorType(UIntType(Width(10)), 8).type_eq(
        VectorType(UIntType(Width(8)), 8)
    )
    assert not VectorType(UIntType(Width(10)), 8).type_eq(
        VectorType(UIntType(Width(10)), 6)
    )
    assert not VectorType(UIntType(Width(10)), 8).type_eq(
        VectorType(SIntType(Width(10)), 8)
    )
    assert not VectorType(UIntType(Width(10)), 8).type_eq(
        VectorType(SIntType(Width(8)), 8)
    )
    assert not VectorType(UIntType(Width(10)), 8).type_eq(
        VectorType(SIntType(Width(10)), 6)
    )
    assert not VectorType(UIntType(Width(10)), 8).type_eq(
        VectorType(UnknownType(), 8)
    )
    assert not VectorType(UIntType(Width(10)), 8).type_eq(
        VectorType(ClockType(), 8)
    )
    assert not VectorType(UIntType(Width(10)), 8).type_eq(
        BundleType([
            Field("a", VectorType(UIntType(Width(10)), 8)),
            Field("b", UIntType(Width(10)))
        ])
    )

    assert not BundleType([
        Field("a", VectorType(UIntType(Width(10)), 8)),
        Field("b", UIntType(Width(10)))
    ]).type_eq(
        BundleType([
            Field("c", VectorType(UIntType(Width(10)), 8)),
            Field("b", UIntType(Width(10)))
        ])
    )
    assert not BundleType([
        Field("a", VectorType(UIntType(Width(10)), 8)),
        Field("b", UIntType(Width(10)))
    ]).type_eq(
        BundleType([
            Field("b", VectorType(UIntType(Width(10)), 8)),
            Field("a", UIntType(Width(10)))
        ])
    )
    assert not BundleType([
        Field("a", VectorType(UIntType(Width(10)), 8)),
        Field("b", UIntType(Width(10)))
    ]).type_eq(
        BundleType([
            Field("a", VectorType(UIntType(Width(8)), 8)),
            Field("b", UIntType(Width(10)))
        ])
    )
    assert not BundleType([
        Field("a", VectorType(UIntType(Width(10)), 8)),
        Field("b", UIntType(Width(10)))
    ]).type_eq(
        BundleType([
            Field("a", VectorType(UIntType(Width(10)), 6)),
            Field("b", UIntType(Width(10)))
        ])
    )

    assert not BundleType([
        Field("a", VectorType(UIntType(Width(10)), 8)),
        Field("b", UIntType(Width(10)))
    ]).type_eq(
        BundleType([
            Field("a", VectorType(SIntType(Width(10)), 8)),
            Field("b", UIntType(Width(10)))
        ])
    )
    assert not BundleType([
        Field("a", VectorType(UIntType(Width(10)), 8)),
        Field("b", UIntType(Width(10)))
    ]).type_eq(
        BundleType([
            Field("a", UnknownType()),
            Field("b", UIntType(Width(10)))
        ])
    )
    assert not BundleType([
        Field("a", VectorType(UIntType(Width(10)), 8)),
        Field("b", UIntType(Width(10)))
    ]).type_eq(
        BundleType([
            Field("b", UnknownType()),
            Field("a", SIntType(Width(10)))
        ])
    )
    assert not BundleType([
        Field("a", VectorType(UIntType(Width(10)), 8)),
        Field("b", UIntType(Width(10)))
    ]).type_eq(
        UIntType(Width(10))
    )
    assert not BundleType([
        Field("a", VectorType(UIntType(Width(10)), 8)),
        Field("b", UIntType(Width(10)))
    ]).type_eq(
        BundleType([
            Field("a", VectorType(UIntType(Width(10)), 8), True),
            Field("b", UIntType(Width(10)), True)
        ])
    )
