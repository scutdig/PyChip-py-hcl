from typing import List

from py_hcl.core.module_factory.inherit_chain.named_expr import NamedExprHolder
from py_hcl.core.module_factory.inherit_chain.stmt_holder import StmtHolder
from py_hcl.transformer.pyhcl_to_firrtl.global_context import GlobalContext
from py_hcl.transformer.pyhcl_to_firrtl.conv_port import convert_ports
from py_hcl.transformer.pyhcl_to_firrtl.conv_stmt import convert_stmt
from py_hcl.transformer.pyhcl_to_firrtl.utils import build_reserve_name, \
    build_io_name, get_io_obj
from py_hcl.core.expr.io import IO
from py_hcl.core.module.packed_module import PackedModule
from py_hcl.firrtl_ir.stmt.block import Block
from py_hcl.firrtl_ir.stmt.defn.module import DefModule


def convert_module(packed_module: PackedModule):
    GlobalContext.expr_id_to_name.update(
        flatten_named_expr_chain(packed_module.named_expr_chain))

    name = packed_module.name
    raw_ports = flatten_io_chain(get_io_obj(packed_module))
    ports = convert_ports(raw_ports)

    stmts = flatten_statement_chain(packed_module.statement_chain)
    final_stmts = [ss for s in stmts for ss in convert_stmt(s)]

    module = DefModule(name, ports, Block(final_stmts))
    GlobalContext.modules[name] = module
    return module


def flatten_named_expr_chain(named_expr_chain: List[NamedExprHolder]):
    named_exprs = {}

    for holder in named_expr_chain:
        for k, v in holder.named_expression_table.items():
            named_exprs[k] = build_reserve_name(holder.module_name, v)

    return named_exprs


def flatten_statement_chain(statement_chain: List[StmtHolder]):
    stmts = []

    for holder in statement_chain:
        for stmt in reversed(holder.top_statement.statements):
            stmts.append(stmt)

    return stmts[::-1]


def flatten_io_chain(io: IO):
    ports = {}

    for io_holder in io.io_chain:
        for k, v in io_holder.named_ports.items():
            ports[build_io_name(io_holder.module_name, k)] = v

    return ports
