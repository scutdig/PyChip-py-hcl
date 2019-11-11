from py_hcl.firrtl_ir import tpe
from tests.test_firrtl_ir.utils import serialize_equal


def test_unknown_type():
    serialize_equal(tpe.UnknownType(), "?")


def test_clock_type():
    serialize_equal(tpe.ClockType(), "Clock")
