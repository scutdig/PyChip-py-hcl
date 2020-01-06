from multipledispatch import dispatch

from py_hcl.core.type import UnknownType as HclUnknownType
from py_hcl.core.type.bundle import BundleT, Dir
from py_hcl.core.type.clock import ClockT
from py_hcl.core.type.sint import SIntT
from py_hcl.core.type.uint import UIntT
from py_hcl.core.type.vector import VectorT
from py_hcl.firrtl_ir.type import SIntType, UIntType, UnknownType, ClockType, \
    VectorType, BundleType
from py_hcl.firrtl_ir.type.field import Field
from py_hcl.firrtl_ir.type.width import Width


@dispatch()
def convert_type(_: HclUnknownType):
    return UnknownType()


@dispatch()
def convert_type(sint: SIntT):
    return SIntType(Width(sint.width))


@dispatch()
def convert_type(uint: UIntT):
    return UIntType(Width(uint.width))


@dispatch()
def convert_type(_: ClockT):
    return ClockType()


@dispatch()
def convert_type(vec: VectorT):
    return VectorType(convert_type(vec.inner_type), vec.size)


@dispatch()
def convert_type(bundle: BundleT):
    fields = []
    for k, v in bundle.fields.items():
        f = Field(k, convert_type(v['hcl_type']), v['dir'] == Dir.SINK)
        fields.append(f)
    return BundleType(fields)
