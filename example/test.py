from functools import reduce

from pyhcl import *

from pyhcl.core._dynamic_ctx import DynamicContext
from pyhcl.core._utils import get_attr
from pyhcl.ir.low_ir import SubField, Connect
from pyhcl.ir.utils import auto_connect


class ModuleA(Module):
    io = IO(
        t_data=Input(U.w(32)),
        in_data=Output(U.w(32)),
        valid=Input(Bool),
        ready=Output(Bool)
    )

    io.in_data <<= io.t_data
    io.ready <<= Bool(True)


class ModuleB(Module):
    io = IO(
        in_data=Input(U.w(32)),
        out_data=Output(U.w(32)),
        valid=Output(Bool),
        ready=Input(Bool)
    )

    io.out_data <<= Mux(io.ready, io.in_data, U(0))
    io.valid <<= Bool(True)


class TopModule(Module):
    io = IO(
        t_data=Input(U.w(32)),
        out_data=Output(U.w(32))
    )

    ma = ModuleA()
    mb = ModuleB()

    auto_connect(ma.io, mb.io)
    io <<= ma.io
    io <<= mb.io


if __name__ == '__main__':
    print(Emitter.emit(TopModule()))
