from multipledispatch import dispatch

from ..utils import type_in
from ...shortcuts import uw
from ...stmt.defn.circuit import DefCircuit
from ...stmt.defn.instance import DefInstance
from ...stmt.defn.memory import DefMemory, DefMemReadPort, DefMemWritePort
from ...stmt.defn.module import DefModule, InputPort, OutputPort, DefExtModule
from ...stmt.defn.node import DefNode
from ...stmt.defn.register import DefRegister, DefInitRegister
from ...stmt.defn.wire import DefWire
from ...type import VectorType, ClockType, UIntType
from ...type_measurer import equal

checker = dispatch


###############################################################
#                      TYPE CHECKERS                          #
###############################################################

@checker(DefWire)
def check(_: DefWire):
    return True


@checker(DefInstance)
def check(_: DefInstance):
    return True


@checker(DefRegister)
def check(reg: DefRegister):
    from ...type_checker import check_all_expr
    if not check_all_expr(reg.clock_ref):
        return False

    if not type_in(reg.clock_ref.tpe, ClockType):
        return False

    return True


@checker(DefInitRegister)
def check(reg: DefInitRegister):
    from ...type_checker import check_all_expr
    if not check_all_expr(reg.clock_ref, reg.reset_ref, reg.init_ref):
        return False

    if not type_in(reg.clock_ref.tpe, ClockType):
        return False

    if not equal(reg.reset_ref.tpe, uw(1)):
        return False

    if not equal(reg.init_ref.tpe, reg.tpe):
        return False

    return True


@checker(DefNode)
def check(node: DefNode):
    from ...type_checker import check_all_expr
    if not check_all_expr(node.expr_ref):
        return False

    return True


@checker(DefMemory)
def check(mem: DefMemory):
    if not type_in(mem.tpe, VectorType):
        return False

    return True


@checker(DefMemReadPort)
def check(mem_read: DefMemReadPort):
    from ...type_checker import check_all_expr
    if not check_all_expr(mem_read.mem_ref, mem_read.index_ref,
                          mem_read.clock_ref):
        return False

    if not type_in(mem_read.mem_ref.tpe, VectorType):
        return False

    if not type_in(mem_read.clock_ref.tpe, ClockType):
        return False

    if not type_in(mem_read.index_ref.tpe, UIntType):
        return False

    return True


@checker(DefMemWritePort)
def check(mem_write: DefMemWritePort):
    from ...type_checker import check_all_expr
    if not check_all_expr(mem_write.mem_ref, mem_write.index_ref,
                          mem_write.clock_ref):
        return False

    if not type_in(mem_write.mem_ref.tpe, VectorType):
        return False

    if not type_in(mem_write.clock_ref.tpe, ClockType):
        return False

    if not type_in(mem_write.index_ref.tpe, UIntType):
        return False

    return True


@checker(DefModule)
def check(mod: DefModule):
    from ...type_checker import check_all_stmt
    if not check_all_stmt(mod.body):
        return False

    if len(mod.ports) == 0:
        return False

    for port in mod.ports:
        if not type_in(port, InputPort, OutputPort):
            return False

    return True


@checker(DefExtModule)
def check(mod: DefExtModule):
    if len(mod.ports) == 0:
        return False

    for port in mod.ports:
        if not type_in(port, InputPort, OutputPort):
            return False

    return True


@checker(DefCircuit)
def check(circuit: DefCircuit):
    from ...type_checker import check_all_stmt
    if not check_all_stmt(*circuit.def_modules):
        return False

    name_found = False
    for mod in circuit.def_modules:
        if not type_in(mod, DefModule, DefExtModule):
            return False
        if mod.name == circuit.main:
            name_found = True

    if not name_found:
        return False

    return True
