from py_hcl.firrtl_ir.expr.mux import Mux
from py_hcl.firrtl_ir.shortcuts import n, uw, u, vec, sw, w
from py_hcl.firrtl_ir.type_checker import check
from ..utils import serialize_equal


def test_mux_basis():
    mux = Mux(n("c", uw(1)), n("a", uw(8)), n("b", uw(8)), uw(8))
    assert check(mux)
    serialize_equal(mux, "mux(c, a, b)")

    mux = Mux(u(1, w(1)),
              n("b", vec(sw(8), 10)),
              n("c", vec(sw(8), 10)),
              vec(sw(8), 10))
    assert check(mux)
    serialize_equal(mux, 'mux(UInt<1>("h1"), b, c)')


def test_mux_cond_type_wrong():
    mux = Mux(n("c", uw(2)), n("a", uw(8)), n("b", uw(8)), uw(8))
    assert not check(mux)

    mux = Mux(n("c", sw(1)), n("a", uw(8)), n("b", uw(8)), uw(8))
    assert not check(mux)

    mux = Mux(n("c", vec(uw(1), 1)), n("a", uw(8)), n("b", uw(8)), uw(8))
    assert not check(mux)


def test_mux_tf_value_type_wrong():
    mux = Mux(n("c", uw(1)), n("a", uw(7)), n("b", uw(8)), uw(8))
    assert not check(mux)

    mux = Mux(n("c", uw(1)), n("a", uw(8)), n("b", sw(8)), uw(8))
    assert not check(mux)

    mux = Mux(n("c", uw(1)), n("a", uw(8)), n("b", uw(8)), sw(8))
    assert not check(mux)
