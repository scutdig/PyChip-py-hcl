from py_hcl.firrtl_ir.expr.accessor import SubField, SubIndex, SubAccess
from py_hcl.firrtl_ir.shortcuts import bdl, uw, sw, n, vec, u, w, s
from py_hcl.firrtl_ir.type_checker import check
from ..utils import serialize_equal


def test_sub_field_basis():
    bd = bdl(a=(uw(8), False), b=(sw(8), False))
    sf = SubField(n("bd", bd), "a", uw(8))
    assert check(sf)
    serialize_equal(sf, "bd.a")

    bd = bdl(a=(bdl(c=(uw(8), True)), False), b=(sw(8), False))
    sf = SubField(n("bd", bd), "a", bdl(c=(uw(8), True)))
    assert check(sf)
    serialize_equal(sf, "bd.a")


def test_sub_field_non_exist():
    bd = bdl(a=(uw(8), False), b=(sw(8), False))
    sf = SubField(n("bd", bd), "c", uw(8))
    assert not check(sf)

    bd = bdl(a=(bdl(c=(uw(8), True)), False), b=(sw(8), False))
    sf = SubField(n("bd", bd), "c", bdl(c=(uw(8), True)))
    assert not check(sf)


def test_sub_field_not_bundle():
    sf = SubField(n("bd", uw(8)), "c", uw(8))
    assert not check(sf)

    sf = SubField(n("bd", vec(uw(8), 32)), "c", bdl(c=(uw(8), True)))
    assert not check(sf)


def test_sub_field_type_wrong():
    bd = bdl(a=(uw(8), False), b=(sw(8), False))
    sf = SubField(n("bd", bd), "a", sw(8))
    assert not check(sf)

    bd = bdl(a=(bdl(c=(uw(8), True)), False), b=(sw(8), False))
    sf = SubField(n("bd", bd), "a", bdl(c=(uw(9), True)))
    assert not check(sf)


def test_sub_index_basis():
    vc = vec(uw(8), 10)
    si = SubIndex(n("vc", vc), 5, uw(8))
    assert check(si)
    serialize_equal(si, "vc[5]")

    vc = vec(vec(uw(8), 10), 20)
    si = SubIndex(n("vc", vc), 19, vec(uw(8), 10))
    assert check(si)
    serialize_equal(si, "vc[19]")


def test_sub_index_over_bound():
    vc = vec(uw(8), 10)
    si = SubIndex(n("vc", vc), 10, uw(8))
    assert not check(si)

    vc = vec(vec(uw(8), 10), 20)
    si = SubIndex(n("vc", vc), -1, vec(uw(8), 10))
    assert not check(si)


def test_sub_index_non_vector():
    si = SubIndex(n("vc", uw(8)), 5, uw(1))
    assert not check(si)

    si = SubIndex(n("vc", bdl(a=(vec(uw(8), 10), True))), 19, vec(uw(8), 10))
    assert not check(si)


def test_sub_index_type_wrong():
    vc = vec(uw(8), 10)
    si = SubIndex(n("vc", vc), 5, sw(8))
    assert not check(si)

    vc = vec(vec(uw(8), 10), 20)
    si = SubIndex(n("vc", vc), 19, vec(uw(8), 20))
    assert not check(si)


def test_sub_access_basis():
    vc = vec(uw(8), 10)
    sa = SubAccess(n("vc", vc), u(2, w(3)), uw(8))
    assert check(sa)
    serialize_equal(sa, 'vc[UInt<3>("2")]')

    vc = vec(uw(8), 10)
    sa = SubAccess(n("vc", vc), n("a", uw(8)), uw(8))
    assert check(sa)
    serialize_equal(sa, 'vc[a]')


def test_sub_access_non_vector():
    sa = SubAccess(n("vc", uw(8)), u(2, w(3)), uw(8))
    assert not check(sa)

    sa = SubAccess(n("vc", bdl(a=(vec(uw(8), 10), True))),
                   u(2, w(3)), vec(uw(8), 10))
    assert not check(sa)


def test_sub_access_idx_non_uint():
    vc = vec(uw(8), 10)
    sa = SubAccess(n("vc", vc), s(2, w(3)), uw(8))
    assert not check(sa)

    vc = vec(uw(8), 10)
    sa = SubAccess(n("vc", vc), n("a", sw(8)), uw(8))
    assert not check(sa)
