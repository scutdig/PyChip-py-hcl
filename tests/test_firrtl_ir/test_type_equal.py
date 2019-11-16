from py_hcl.firrtl_ir.shortcuts import uw, sw, vec, bdl
from py_hcl.firrtl_ir.type import UnknownType, ClockType
from py_hcl.firrtl_ir.type_measurer import equal


def test_type_eq():
    assert equal(UnknownType(), UnknownType())
    assert equal(ClockType(), ClockType())
    assert equal(uw(10), uw(10))
    assert equal(sw(10), sw(10))
    assert equal(vec(uw(10), 8), vec(uw(10), 8))
    assert equal(bdl(a=(vec(uw(10), 8), False), b=(uw(10), True)),
                 bdl(a=(vec(uw(10), 8), False), b=(uw(10), True)))


def test_type_neq():
    assert not equal(UnknownType(), ClockType())
    assert not equal(UnknownType(), uw(10))
    assert not equal(UnknownType(), sw(10))
    assert not equal(UnknownType(), vec(uw(10), 8))
    assert not equal(UnknownType(), vec(sw(10), 8))
    assert not equal(UnknownType(),
                     bdl(a=(vec(uw(10), 8), False), b=(uw(10), False)))

    assert not equal(ClockType(), UnknownType())
    assert not equal(ClockType(), uw(10))
    assert not equal(ClockType(), sw(10))
    assert not equal(ClockType(), vec(uw(10), 8))
    assert not equal(ClockType(), vec(sw(10), 8))
    assert not equal(ClockType(),
                     bdl(a=(vec(uw(10), 8), False), b=(uw(10), False)))

    assert not equal(uw(10), UnknownType())
    assert not equal(uw(10), ClockType())
    assert not equal(uw(10), uw(8))
    assert not equal(uw(10), sw(10))
    assert not equal(uw(10), sw(10))
    assert not equal(uw(10), vec(uw(10), 8))
    assert not equal(uw(10), vec(sw(10), 8))
    assert not equal(uw(10),
                     bdl(a=(vec(uw(10), 8), False), b=(uw(10), False)))

    assert not equal(sw(10), UnknownType())
    assert not equal(sw(10), ClockType())
    assert not equal(sw(10), sw(8))
    assert not equal(sw(10), uw(10))
    assert not equal(sw(10), uw(10))
    assert not equal(sw(10), vec(uw(10), 8))
    assert not equal(sw(10), vec(sw(10), 8))
    assert not equal(sw(10),
                     bdl(a=(vec(uw(10), 8), False), b=(uw(10), False)))

    assert not equal(vec(uw(10), 8), UnknownType())
    assert not equal(vec(uw(10), 8), ClockType())
    assert not equal(vec(uw(10), 8), sw(8))
    assert not equal(vec(uw(10), 8), uw(10))
    assert not equal(vec(uw(10), 8), uw(10))
    assert not equal(vec(uw(10), 8), vec(uw(8), 8))
    assert not equal(vec(uw(10), 8), vec(uw(10), 9))
    assert not equal(vec(uw(10), 8), vec(sw(10), 8))
    assert not equal(vec(uw(10), 8),
                     bdl(a=(vec(uw(10), 8), False), b=(uw(10), False)))

    assert not equal(bdl(a=(vec(uw(10), 8), False), b=(uw(10), False)),
                     UnknownType())
    assert not equal(bdl(a=(vec(uw(10), 8), False), b=(uw(10), False)),
                     ClockType())
    assert not equal(bdl(a=(vec(uw(10), 8), False), b=(uw(10), False)),
                     sw(8))
    assert not equal(bdl(a=(vec(uw(10), 8), False), b=(uw(10), False)),
                     uw(10))
    assert not equal(bdl(a=(vec(uw(10), 8), False), b=(uw(10), False)),
                     uw(10))
    assert not equal(bdl(a=(vec(uw(10), 8), False), b=(uw(10), False)),
                     vec(sw(10), 8))
    assert not equal(bdl(a=(vec(uw(10), 8), False), b=(uw(10), False)),
                     bdl(a=(vec(uw(10), 8), True), b=(uw(10), False)))
    assert not equal(bdl(a=(vec(uw(10), 8), False), b=(uw(10), False)),
                     bdl(a=(vec(uw(10), 2), False), b=(uw(10), False)))
    assert not equal(bdl(a=(uw(3), False), b=(uw(10), False)),
                     bdl(a=(uw(3), False), b=(uw(10), False), c=(sw(2), True)))
    assert not equal(bdl(a=(vec(uw(10), 8), False), b=(uw(10), False)),
                     bdl(b=(uw(10), False), a=(vec(uw(10), 8), False)))
