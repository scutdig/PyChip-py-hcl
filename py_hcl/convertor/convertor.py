from py_hcl.convertor.context import Context
from py_hcl.convertor.conv_module import convert_module
from py_hcl.core.module.packed_module import PackedModule
from py_hcl.firrtl_ir.stmt.defn.circuit import DefCircuit
from py_hcl.firrtl_ir.type_checker import check


def convert(packed_module: PackedModule):
    convert_module(packed_module)
    modules = list(Context.modules.values())
    Context.modules.clear()
    Context.expr_obj_id_to_ref.clear()
    Context.expr_id_to_name.clear()
    cir = DefCircuit(packed_module.name, modules)
    assert check(cir)
    return cir
