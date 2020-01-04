from py_hcl.convertor.context import Context
from py_hcl.convertor.conv_port import convert_ports
from py_hcl.convertor.conv_stmt import convert_stmt
from py_hcl.convertor.utils import build_reserve_name, \
    build_io_name, get_io_obj
from py_hcl.core.expr.io import IO
from py_hcl.core.module.packed_module import PackedModule
from py_hcl.core.module_factory.inherit_list.named_expr import NamedExprChain
from py_hcl.core.module_factory.inherit_list.stmt_holder import StmtChain
from py_hcl.firrtl_ir.stmt.block import Block
from py_hcl.firrtl_ir.stmt.defn.module import DefModule


def convert_module(packed_module: PackedModule):
    Context.expr_id_to_name.update(
        flatten_named_expr_chain(packed_module.named_expr_chain))

    name = packed_module.name
    raw_ports = flatten_io_chain(get_io_obj(packed_module))
    ports = convert_ports(raw_ports)

    stmts = flatten_statement_chain(packed_module.statement_chain)
    final_stmts = [ss for s in stmts for ss in convert_stmt(s)]

    module = DefModule(name, ports, Block(final_stmts))
    Context.modules[name] = module
    return module


def flatten_named_expr_chain(named_expr_chain: NamedExprChain):
    named_exprs = {}
    node = named_expr_chain.named_expr_chain_head

    while True:
        holder = node.named_expr_holder
        for k, v in holder.named_expression_table.items():
            named_exprs[k] = build_reserve_name(holder.module_name, v)

        if not hasattr(node, "next_node"):
            break
        node = node.next_node

    return named_exprs


def flatten_statement_chain(statement_chain: StmtChain):
    stmts = []
    node = statement_chain.stmt_chain_head

    while True:
        holder = node.stmt_holder
        for stmt in reversed(holder.top_statement.statements):
            stmts.append(stmt)

        if not hasattr(node, "next_node"):
            break
        node = node.next_node

    return list(reversed(stmts))


def flatten_io_chain(io: IO):
    ports = {}
    node = io.io_chain_head

    while True:
        holder = node.io_holder
        # reverse the dict order
        for k in list(holder.named_ports.keys())[::-1]:
            v = holder.named_ports[k]
            ports[build_io_name(holder.module_name, k)] = v

        if not hasattr(node, "next_node"):
            break
        node = node.next_node

    return {k: ports[k] for k in list(ports.keys())[::-1]}
