from ...shortcuts import uw
from ...type_measurer import equal
from ...stmt.defn.circuit import DefCircuit
from ...stmt.defn.instance import DefInstance
from ...stmt.defn.memory import DefMemory, DefMemReadPort, DefMemWritePort
from ...stmt.defn.module import DefModule, InputPort, OutputPort, DefExtModule
from ...stmt.defn.node import DefNode
from ...type import VectorType, ClockType, UIntType
from ..utils import type_in
from ...stmt.defn.register import DefRegister, DefInitRegister
from ...stmt.defn.wire import DefWire


class DefinitionTypeChecker(object):
    definition_checker_map = {}

    @staticmethod
    def check(op_obj):
        try:
            return DefinitionTypeChecker \
                .definition_checker_map[type(op_obj)](op_obj)
        except KeyError:
            raise NotImplementedError(type(op_obj))


def checker(definition):
    def f(func):
        DefinitionTypeChecker.definition_checker_map[definition] = func
        return func

    return f


###############################################################
#                      TYPE CHECKERS                          #
###############################################################

@checker(DefWire)
def _(_):
    return True


@checker(DefInstance)
def _(_):
    return True


@checker(DefRegister)
def _(reg):
    from ...type_checker import check_all_expr
    if not check_all_expr(reg.clock_ref):
        return False

    if not type_in(reg.clock_ref.tpe, ClockType):
        return False

    return True


@checker(DefInitRegister)
def _(reg):
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
def _(node):
    from ...type_checker import check_all_expr
    if not check_all_expr(node.expr_ref):
        return False

    return True


@checker(DefMemory)
def _(mem):
    if not type_in(mem.tpe, VectorType):
        return False

    return True


@checker(DefMemReadPort)
def _(mem_read):
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
def _(mem_write):
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
def _(mod):
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
def _(mod):
    if len(mod.ports) == 0:
        return False

    for port in mod.ports:
        if not type_in(port, InputPort, OutputPort):
            return False

    return True


@checker(DefCircuit)
def _(circuit):
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
