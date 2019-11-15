from py_hcl.firrtl_ir.field import Field
from py_hcl.firrtl_ir.tpe import UnknownType, ClockType, \
    UIntType, SIntType, VectorType, BundleType
from py_hcl.firrtl_ir.width import IntWidth, UnknownWidth


def test_type_eq():
    assert UnknownType().type_eq(
        UnknownType()
    )
    assert ClockType().type_eq(
        ClockType()
    )
    assert UIntType(IntWidth(10)).type_eq(
        UIntType(IntWidth(10))
    )
    assert UIntType(UnknownWidth()).type_eq(
        UIntType(UnknownWidth())
    )
    assert SIntType(IntWidth(10)).type_eq(
        SIntType(IntWidth(10))
    )
    assert SIntType(UnknownWidth()).type_eq(
        SIntType(UnknownWidth())
    )
    assert VectorType(UIntType(IntWidth(10)), 8).type_eq(
        VectorType(UIntType(IntWidth(10)), 8)
    )
    assert BundleType([
        Field("a", VectorType(UIntType(IntWidth(10)), 8)),
        Field("b", UIntType(IntWidth(10)))
    ]).type_eq(
        BundleType([
            Field("a", VectorType(UIntType(IntWidth(10)), 8)),
            Field("b", UIntType(IntWidth(10)))
        ])
    )


def test_type_neq():
    assert not UnknownType().type_eq(
        ClockType()
    )
    assert not UnknownType().type_eq(UIntType(
        IntWidth(10))
    )
    assert not UnknownType().type_eq(UIntType(
        UnknownWidth())
    )
    assert not UnknownType().type_eq(SIntType(
        IntWidth(10))
    )
    assert not UnknownType().type_eq(SIntType(
        UnknownWidth())
    )
    assert not UnknownType().type_eq(VectorType(
        UIntType(IntWidth(10)), 8)
    )
    assert not UnknownType().type_eq(VectorType(
        UIntType(UnknownWidth()), 8)
    )
    assert not UnknownType().type_eq(VectorType(
        SIntType(IntWidth(10)), 8)
    )
    assert not UnknownType().type_eq(VectorType(
        SIntType(UnknownWidth()), 8)
    )
    assert not UnknownType().type_eq(
        BundleType([
            Field("a", VectorType(UIntType(IntWidth(10)), 8)),
            Field("b", UIntType(IntWidth(10)))
        ])
    )

    assert not ClockType().type_eq(
        UIntType(IntWidth(10))
    )
    assert not ClockType().type_eq(
        UIntType(UnknownWidth())
    )
    assert not ClockType().type_eq(
        SIntType(IntWidth(10))
    )
    assert not ClockType().type_eq(
        SIntType(UnknownWidth())
    )
    assert not ClockType().type_eq(
        VectorType(UIntType(IntWidth(10)), 8)

    )
    assert not ClockType().type_eq(
        VectorType(UIntType(UnknownWidth()), 8)
    )
    assert not ClockType().type_eq(
        VectorType(SIntType(IntWidth(10)), 8)
    )
    assert not ClockType().type_eq(
        VectorType(SIntType(UnknownWidth()), 8)
    )
    assert not ClockType().type_eq(
        BundleType([
            Field("a", VectorType(UIntType(IntWidth(10)), 8)),
            Field("b", UIntType(IntWidth(10)))
        ])
    )

    assert not UIntType(IntWidth(10)).type_eq(
        UIntType(UnknownWidth())
    )
    assert not UIntType(UnknownWidth()).type_eq(
        UIntType(IntWidth(10))
    )
    assert not UIntType(IntWidth(10)).type_eq(
        UIntType(IntWidth(8))
    )
    assert not UIntType(IntWidth(10)).type_eq(
        SIntType(IntWidth(10))
    )
    assert not UIntType(IntWidth(10)).type_eq(
        SIntType(UnknownWidth())
    )
    assert not UIntType(IntWidth(10)).type_eq(
        VectorType(UIntType(IntWidth(10)), 8)
    )
    assert not UIntType(IntWidth(10)).type_eq(
        VectorType(UIntType(UnknownWidth()), 8)
    )
    assert not UIntType(IntWidth(10)).type_eq(
        VectorType(SIntType(IntWidth(10)), 8)
    )
    assert not UIntType(IntWidth(10)).type_eq(
        VectorType(SIntType(UnknownWidth()), 8)
    )
    assert not UIntType(IntWidth(10)).type_eq(
        BundleType([
            Field("a", VectorType(UIntType(IntWidth(10)), 8)),
            Field("b", UIntType(IntWidth(10)))
        ])
    )

    assert not UIntType(UnknownWidth()).type_eq(
        SIntType(IntWidth(10))
    )
    assert not UIntType(UnknownWidth()).type_eq(
        SIntType(UnknownWidth())
    )
    assert not UIntType(UnknownWidth()).type_eq(
        VectorType(UIntType(IntWidth(10)), 8)
    )
    assert not UIntType(UnknownWidth()).type_eq(
        VectorType(UIntType(UnknownWidth()), 8)
    )
    assert not UIntType(UnknownWidth()).type_eq(
        VectorType(SIntType(IntWidth(10)), 8)
    )
    assert not UIntType(UnknownWidth()).type_eq(
        VectorType(SIntType(UnknownWidth()), 8)
    )
    assert not UIntType(UnknownWidth()).type_eq(
        BundleType([
            Field("a", VectorType(UIntType(IntWidth(10)), 8)),
            Field("b", UIntType(IntWidth(10)))
        ])
    )

    assert not SIntType(IntWidth(10)).type_eq(
        SIntType(UnknownWidth())
    )
    assert not SIntType(IntWidth(10)).type_eq(
        SIntType(IntWidth(8))
    )
    assert not SIntType(IntWidth(10)).type_eq(
        VectorType(UIntType(IntWidth(10)), 8)
    )
    assert not SIntType(IntWidth(10)).type_eq(
        VectorType(UIntType(UnknownWidth()), 8)

    )
    assert not SIntType(IntWidth(10)).type_eq(
        VectorType(SIntType(IntWidth(10)), 8)
    )
    assert not SIntType(IntWidth(10)).type_eq(
        VectorType(SIntType(UnknownWidth()), 8)
    )
    assert not SIntType(IntWidth(10)).type_eq(
        BundleType([
            Field("a", VectorType(UIntType(IntWidth(10)), 8)),
            Field("b", UIntType(IntWidth(10)))
        ])
    )

    assert not SIntType(UnknownWidth()).type_eq(
        VectorType(UIntType(IntWidth(10)), 8)
    )
    assert not SIntType(UnknownWidth()).type_eq(
        VectorType(UIntType(UnknownWidth()), 8)
    )
    assert not SIntType(UnknownWidth()).type_eq(
        VectorType(SIntType(IntWidth(10)), 8)
    )
    assert not SIntType(UnknownWidth()).type_eq(
        VectorType(SIntType(UnknownWidth()), 8)
    )
    assert not SIntType(UnknownWidth()).type_eq(
        BundleType([
            Field("a", VectorType(UIntType(IntWidth(10)), 8)),
            Field("b", UIntType(IntWidth(10)))
        ])
    )

    assert not VectorType(UIntType(IntWidth(10)), 8).type_eq(
        VectorType(UIntType(IntWidth(8)), 8)
    )
    assert not VectorType(UIntType(IntWidth(10)), 8).type_eq(
        VectorType(UIntType(IntWidth(10)), 6)
    )
    assert not VectorType(UIntType(IntWidth(10)), 8).type_eq(
        VectorType(UIntType(UnknownWidth()), 8)
    )
    assert not VectorType(UIntType(IntWidth(10)), 8).type_eq(
        VectorType(SIntType(IntWidth(10)), 8)
    )
    assert not VectorType(UIntType(IntWidth(10)), 8).type_eq(
        VectorType(SIntType(IntWidth(8)), 8)
    )
    assert not VectorType(UIntType(IntWidth(10)), 8).type_eq(
        VectorType(SIntType(IntWidth(10)), 6)
    )
    assert not VectorType(UIntType(IntWidth(10)), 8).type_eq(
        VectorType(SIntType(UnknownWidth()), 8)
    )
    assert not VectorType(UIntType(IntWidth(10)), 8).type_eq(
        VectorType(UnknownType(), 8)
    )
    assert not VectorType(UIntType(IntWidth(10)), 8).type_eq(
        VectorType(ClockType(), 8)
    )
    assert not VectorType(UIntType(IntWidth(10)), 8).type_eq(
        BundleType([
            Field("a", VectorType(UIntType(IntWidth(10)), 8)),
            Field("b", UIntType(IntWidth(10)))
        ])
    )

    assert not BundleType([
        Field("a", VectorType(UIntType(IntWidth(10)), 8)),
        Field("b", UIntType(IntWidth(10)))
    ]).type_eq(
        BundleType([
            Field("c", VectorType(UIntType(IntWidth(10)), 8)),
            Field("b", UIntType(IntWidth(10)))
        ])
    )
    assert not BundleType([
        Field("a", VectorType(UIntType(IntWidth(10)), 8)),
        Field("b", UIntType(IntWidth(10)))
    ]).type_eq(
        BundleType([
            Field("b", VectorType(UIntType(IntWidth(10)), 8)),
            Field("a", UIntType(IntWidth(10)))
        ])
    )
    assert not BundleType([
        Field("a", VectorType(UIntType(IntWidth(10)), 8)),
        Field("b", UIntType(IntWidth(10)))
    ]).type_eq(
        BundleType([
            Field("a", VectorType(UIntType(IntWidth(8)), 8)),
            Field("b", UIntType(IntWidth(10)))
        ])
    )
    assert not BundleType([
        Field("a", VectorType(UIntType(IntWidth(10)), 8)),
        Field("b", UIntType(IntWidth(10)))
    ]).type_eq(
        BundleType([
            Field("a", VectorType(UIntType(IntWidth(10)), 6)),
            Field("b", UIntType(IntWidth(10)))
        ])
    )
    assert not BundleType([
        Field("a", VectorType(UIntType(IntWidth(10)), 8)),
        Field("b", UIntType(IntWidth(10)))
    ]).type_eq(
        BundleType([
            Field("a", VectorType(UIntType(UnknownWidth()), 8)),
            Field("b", UIntType(IntWidth(10)))
        ])
    )
    assert not BundleType([
        Field("a", VectorType(UIntType(IntWidth(10)), 8)),
        Field("b", UIntType(IntWidth(10)))
    ]).type_eq(
        BundleType([
            Field("a", VectorType(SIntType(IntWidth(10)), 8)),
            Field("b", UIntType(IntWidth(10)))
        ])
    )
    assert not BundleType([
        Field("a", VectorType(UIntType(IntWidth(10)), 8)),
        Field("b", UIntType(IntWidth(10)))
    ]).type_eq(
        BundleType([
            Field("a", UnknownType()),
            Field("b", UIntType(IntWidth(10)))
        ])
    )
    assert not BundleType([
        Field("a", VectorType(UIntType(IntWidth(10)), 8)),
        Field("b", UIntType(IntWidth(10)))
    ]).type_eq(
        BundleType([
            Field("b", UnknownType()),
            Field("a", SIntType(IntWidth(10)))
        ])
    )
    assert not BundleType([
        Field("a", VectorType(UIntType(IntWidth(10)), 8)),
        Field("b", UIntType(IntWidth(10)))
    ]).type_eq(
        UIntType(IntWidth(10))
    )
    assert not BundleType([
        Field("a", VectorType(UIntType(IntWidth(10)), 8)),
        Field("b", UIntType(IntWidth(10)))
    ]).type_eq(
        BundleType([
            Field("a", VectorType(UIntType(IntWidth(10)), 8), True),
            Field("b", UIntType(IntWidth(10)), True)
        ])
    )
