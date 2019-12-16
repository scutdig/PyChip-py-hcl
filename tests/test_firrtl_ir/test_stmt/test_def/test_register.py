from py_hcl.firrtl_ir.shortcuts import n, s, w, vec, uw, sw, u
from py_hcl.firrtl_ir.stmt.defn.register import DefRegister, DefInitRegister
from py_hcl.firrtl_ir.type import ClockType
from py_hcl.firrtl_ir.type_checker import check
from ...utils import serialize_stmt_equal


def test_register_basis():
    r1 = DefRegister("r1", uw(8), n("clock", ClockType()))
    assert check(r1)
    serialize_stmt_equal(r1, 'reg r1 : UInt<8>, clock')

    r2 = DefRegister("r2", vec(uw(8), 10), n("clock", ClockType()))
    assert check(r2)
    serialize_stmt_equal(r2, 'reg r2 : UInt<8>[10], clock')


def test_register_clock_wrong():
    r1 = DefRegister("r1", uw(8), n("clock", uw(1)))
    assert not check(r1)

    r2 = DefRegister("r2", vec(uw(8), 10), n("clock", sw(1)))
    assert not check(r2)


def test_init_register_basis():
    r1 = DefInitRegister("r1", uw(8),
                         n("clock", ClockType()), n("r", uw(1)), u(5, w(8)))
    assert check(r1)
    serialize_stmt_equal(r1, 'reg r1 : UInt<8>, clock with :\n'
                             '  reset => (r, UInt<8>("5"))')

    r2 = DefInitRegister("r2", sw(8),
                         n("clock", ClockType()), u(0, w(1)), s(5, w(8)))
    assert check(r2)
    serialize_stmt_equal(r2, 'reg r2 : SInt<8>, clock with :\n'
                             '  reset => (UInt<1>("0"), SInt<8>("5"))')


def test_init_register_clock_wrong():
    r1 = DefInitRegister("r1", uw(8),
                         n("clock", uw(1)), n("r", uw(1)), u(5, w(8)))
    assert not check(r1)

    r2 = DefInitRegister("r2", sw(8),
                         n("clock", sw(1)), u(0, w(1)), s(5, w(8)))
    assert not check(r2)


def test_init_register_reset_wrong():
    r1 = DefInitRegister("r1", uw(8),
                         n("clock", ClockType()), n("r", sw(1)), u(5, w(8)))
    assert not check(r1)

    r2 = DefInitRegister("r2", sw(8),
                         n("clock", ClockType()), s(0, w(1)), s(5, w(8)))
    assert not check(r2)


def test_init_register_type_not_match():
    r1 = DefInitRegister("r1", uw(8),
                         n("clock", ClockType()), n("r", uw(1)), s(5, w(8)))
    assert not check(r1)

    r2 = DefInitRegister("r2", uw(8),
                         n("clock", ClockType()), u(0, w(1)), s(5, w(8)))
    assert not check(r2)
