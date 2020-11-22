from py_hcl.transformer.pyhcl_to_firrtl.global_context import GlobalContext
from py_hcl.transformer.pyhcl_to_firrtl.conv_module import convert_module
from py_hcl.core.module.packed_module import PackedModule
from py_hcl.firrtl_ir.stmt.defn.circuit import DefCircuit
from py_hcl.firrtl_ir.type_checker import check


def convert(packed_module: PackedModule):
    convert_module(packed_module)
    modules = list(GlobalContext.modules.values())

    GlobalContext.clear()

    cir = DefCircuit(packed_module.name, modules)
    assert check(cir)
    return cir
