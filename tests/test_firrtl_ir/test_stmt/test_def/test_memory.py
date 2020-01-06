from py_hcl.firrtl_ir.shortcuts import vec, uw, bdl, n, u, w, s
from py_hcl.firrtl_ir.stmt.defn.memory import DefMemory, \
    DefMemWritePort, DefMemReadPort
from py_hcl.firrtl_ir.type import ClockType
from py_hcl.firrtl_ir.type_checker import check
from ...utils import serialize_stmt_equal


def test_memory_basis():
    mem = DefMemory("m", vec(uw(8), 10))
    assert check(mem)
    serialize_stmt_equal(mem, 'cmem m : UInt<8>[10]')

    mem = DefMemory("m", vec(bdl(a=(uw(8), False)), 10))
    assert check(mem)
    serialize_stmt_equal(mem, 'cmem m : {a : UInt<8>}[10]')


def test_memory_type_wrong():
    mem = DefMemory("m", bdl(a=(vec(uw(8), 10), False)))
    assert not check(mem)

    mem = DefMemory("m", uw(9))
    assert not check(mem)


def test_read_port_basis():
    mem_ref = n("m", vec(uw(8), 10))
    mr = DefMemReadPort("mr", mem_ref, u(2, w(8)), n("clock", ClockType()))
    assert check(mr)
    serialize_stmt_equal(mr, 'read mport mr = m[UInt<8>("h2")], clock')

    mem_ref = n("m", vec(bdl(a=(uw(8), False)), 10))
    mr = DefMemReadPort("mr", mem_ref, n("a", uw(2)), n("clock", ClockType()))
    assert check(mr)
    serialize_stmt_equal(mr, 'read mport mr = m[a], clock')


def test_read_port_clock_wrong():
    mem_ref = n("m", vec(uw(8), 10))
    mr = DefMemReadPort("mr", mem_ref, u(2, w(8)), n("clock", uw(1)))
    assert not check(mr)

    mem_ref = n("m", vec(bdl(a=(uw(8), False)), 10))
    mr = DefMemReadPort("mr", mem_ref, n("a", uw(2)), u(0, w(1)))
    assert not check(mr)


def test_read_port_index_wrong():
    mem_ref = n("m", vec(uw(8), 10))
    mr = DefMemReadPort("mr", mem_ref, s(2, w(8)), n("clock", ClockType()))
    assert not check(mr)

    mem_ref = n("m", vec(bdl(a=(uw(8), False)), 10))
    mr = DefMemReadPort("mr", mem_ref,
                        n("a", vec(uw(1), 10)), n("clock", ClockType()))
    assert not check(mr)


def test_read_port_mem_wrong():
    mem_ref = n("m", bdl(a=(vec(uw(8), 10), False)))
    mr = DefMemReadPort("mr", mem_ref, u(2, w(8)), n("clock", ClockType()))
    assert not check(mr)

    mem_ref = n("m", uw(9))
    mr = DefMemReadPort("mr", mem_ref, n("a", uw(2)), n("clock", ClockType()))
    assert not check(mr)


def test_write_port_basis():
    mem_ref = n("m", vec(uw(8), 10))
    mw = DefMemWritePort("mw", mem_ref, u(2, w(8)), n("clock", ClockType()))
    assert check(mw)
    serialize_stmt_equal(mw, 'write mport mw = m[UInt<8>("h2")], clock')

    mem_ref = n("m", vec(bdl(a=(uw(8), False)), 10))
    mw = DefMemWritePort("mw", mem_ref, n("a", uw(2)), n("clock", ClockType()))
    assert check(mw)
    serialize_stmt_equal(mw, 'write mport mw = m[a], clock')


def test_write_port_clock_wrong():
    mem_ref = n("m", vec(uw(8), 10))
    mw = DefMemWritePort("mw", mem_ref, u(2, w(8)), n("clock", uw(1)))
    assert not check(mw)

    mem_ref = n("m", vec(bdl(a=(uw(8), False)), 10))
    mw = DefMemWritePort("mw", mem_ref, n("a", uw(2)), u(0, w(1)))
    assert not check(mw)


def test_write_port_index_wrong():
    mem_ref = n("m", vec(uw(8), 10))
    mw = DefMemWritePort("mw", mem_ref, s(2, w(8)), n("clock", ClockType()))
    assert not check(mw)

    mem_ref = n("m", vec(bdl(a=(uw(8), False)), 10))
    mw = DefMemWritePort("mw", mem_ref,
                         n("a", vec(uw(1), 10)), n("clock", ClockType()))
    assert not check(mw)


def test_write_port_mem_wrong():
    mem_ref = n("m", bdl(a=(vec(uw(8), 10), False)))
    mw = DefMemWritePort("mw", mem_ref, u(2, w(8)), n("clock", ClockType()))
    assert not check(mw)

    mem_ref = n("m", uw(9))
    mw = DefMemWritePort("mw", mem_ref,
                         n("a", uw(2)), n("clock", ClockType()))
    assert not check(mw)
