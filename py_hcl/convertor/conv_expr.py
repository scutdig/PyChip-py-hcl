import copy

from multipledispatch import dispatch

from py_hcl.convertor.context import Context
from py_hcl.convertor.conv_port import ports_to_bundle_type
from py_hcl.convertor.conv_type import convert_type
from py_hcl.convertor.utils import build_io_name, get_io_obj
from py_hcl.core.expr import ExprHolder
from py_hcl.core.expr.add import Add as CAdd
from py_hcl.core.expr.and_ import And as CAnd
from py_hcl.core.expr.xor import Xor as CXor
from py_hcl.core.expr.or_ import Or as COr
from py_hcl.core.expr.convert import ToSInt, ToUInt
from py_hcl.core.expr.extend import Extend
from py_hcl.core.expr.field import FieldAccess
from py_hcl.core.expr.index import VecIndex
from py_hcl.core.expr.io import IO
from py_hcl.core.expr.lit_sint import SLiteral
from py_hcl.core.expr.lit_uint import ULiteral
from py_hcl.core.expr.mod_inst import ModuleInst
from py_hcl.core.expr.slice import Bits as CBits
from py_hcl.core.expr.wire import Wire
from py_hcl.firrtl_ir.expr.accessor import SubField, SubIndex
from py_hcl.firrtl_ir.expr.literal import UIntLiteral, SIntLiteral
from py_hcl.firrtl_ir.expr.prim_ops import Add, Bits, AsSInt, AsUInt, \
    And, Xor, Or
from py_hcl.firrtl_ir.expr.reference import Reference
from py_hcl.firrtl_ir.stmt.connect import Connect
from py_hcl.firrtl_ir.stmt.defn.instance import DefInstance
from py_hcl.firrtl_ir.stmt.defn.node import DefNode
from py_hcl.firrtl_ir.stmt.defn.wire import DefWire
from py_hcl.firrtl_ir.type import ClockType, UIntType
from py_hcl.firrtl_ir.type.width import Width


def convert_expr_by_id(expr_id: int):
    obj = Context.expr_table[expr_id]
    if id(obj) in Context.expr_obj_id_to_ref:
        return [], Context.expr_obj_id_to_ref[id(obj)]

    return convert_expr(obj)


@dispatch()
def convert_expr_op(expr_holder: ExprHolder, add: CAdd):
    l_stmts, l_ref = convert_expr_by_id(add.left_expr_id)
    r_stmts, r_ref = convert_expr_by_id(add.right_expr_id)
    name = NameGetter.get(expr_holder.id)
    typ = convert_type(expr_holder.hcl_type)
    stmt, ref = save_node_ref(Add([l_ref, r_ref], typ),
                              name, typ, id(expr_holder))
    return [*l_stmts, *r_stmts, stmt], ref


@dispatch()
def convert_expr_op(expr_holder: ExprHolder, and_: CAnd):
    l_stmts, l_ref = convert_expr_by_id(and_.left_expr_id)
    r_stmts, r_ref = convert_expr_by_id(and_.right_expr_id)
    name = NameGetter.get(expr_holder.id)
    typ = convert_type(expr_holder.hcl_type)
    stmt, ref = save_node_ref(And([l_ref, r_ref], typ),
                              name, typ, id(expr_holder))
    return [*l_stmts, *r_stmts, stmt], ref


@dispatch()
def convert_expr_op(expr_holder: ExprHolder, xor: CXor):
    l_stmts, l_ref = convert_expr_by_id(xor.left_expr_id)
    r_stmts, r_ref = convert_expr_by_id(xor.right_expr_id)
    name = NameGetter.get(expr_holder.id)
    typ = convert_type(expr_holder.hcl_type)
    stmt, ref = save_node_ref(Xor([l_ref, r_ref], typ),
                              name, typ, id(expr_holder))
    return [*l_stmts, *r_stmts, stmt], ref


@dispatch()
def convert_expr_op(expr_holder: ExprHolder, or_: COr):
    l_stmts, l_ref = convert_expr_by_id(or_.left_expr_id)
    r_stmts, r_ref = convert_expr_by_id(or_.right_expr_id)
    name = NameGetter.get(expr_holder.id)
    typ = convert_type(expr_holder.hcl_type)
    stmt, ref = save_node_ref(Or([l_ref, r_ref], typ),
                              name, typ, id(expr_holder))
    return [*l_stmts, *r_stmts, stmt], ref


@dispatch()
def convert_expr_op(expr_holder: ExprHolder, bs: CBits):
    stmts, v_ref = convert_expr_by_id(bs.ref_expr_id)
    name = NameGetter.get(expr_holder.id)
    typ = convert_type(expr_holder.hcl_type)
    stmt, ref = save_node_ref(Bits(v_ref, [bs.high, bs.low], typ),
                              name, typ, id(expr_holder))
    return [*stmts, stmt], ref


@dispatch()
def convert_expr_op(expr_holder: ExprHolder, ts: ToSInt):
    stmts, v_ref = convert_expr_by_id(ts.ref_expr_id)
    name = NameGetter.get(expr_holder.id)
    typ = convert_type(expr_holder.hcl_type)
    stmt, ref = save_node_ref(AsSInt(v_ref, typ),
                              name, typ, id(expr_holder))
    return [*stmts, stmt], ref


@dispatch()
def convert_expr_op(expr_holder: ExprHolder, tu: ToUInt):
    stmts, v_ref = convert_expr_by_id(tu.ref_expr_id)
    name = NameGetter.get(expr_holder.id)
    typ = convert_type(expr_holder.hcl_type)
    stmt, ref = save_node_ref(AsUInt(v_ref, typ),
                              name, typ, id(expr_holder))
    return [*stmts, stmt], ref


@dispatch()
def convert_expr_op(expr_holder: ExprHolder, et: Extend):
    stmts, v_ref = convert_expr_by_id(et.ref_expr_id)
    typ = convert_type(expr_holder.hcl_type)
    ref = copy.copy(v_ref)
    ref.tpe = typ
    Context.expr_obj_id_to_ref[id(expr_holder)] = ref
    return stmts, ref


@dispatch()
def convert_expr_op(expr_holder: ExprHolder, vi: VecIndex):
    stmts, v_ref = convert_expr_by_id(vi.ref_expr_id)
    ref = SubIndex(v_ref, vi.index, convert_type(expr_holder.hcl_type))
    Context.expr_obj_id_to_ref[id(expr_holder)] = ref
    return stmts, ref


@dispatch()
def convert_expr_op(expr_holder: ExprHolder, fa: FieldAccess):
    typ = convert_type(expr_holder.hcl_type)
    obj = Context.expr_table[fa.ref_expr_id]

    def fetch_current_io_holder(obj):
        current_node = obj.io_chain_head
        while True:
            if fa.item in current_node.io_holder.named_ports:
                return current_node.io_holder
            current_node = current_node.next_node

    if isinstance(obj, IO):
        io_holder = fetch_current_io_holder(obj)
        name = build_io_name(io_holder.module_name, fa.item)
        ref = Reference(name, typ)
        Context.expr_obj_id_to_ref[id(expr_holder)] = ref
        return [], ref

    elif isinstance(obj, ModuleInst):
        stmts, b_ref = convert_expr_by_id(obj.id)
        io_holder = fetch_current_io_holder(get_io_obj(obj.packed_module))
        name = build_io_name(io_holder.module_name, fa.item)
        ref = SubField(b_ref, name, typ)
        Context.expr_obj_id_to_ref[id(expr_holder)] = ref
        return stmts, ref

    else:
        stmts, src_ref = convert_expr_by_id(fa.ref_expr_id)
        ref = SubField(src_ref, fa.item, typ)
        Context.expr_obj_id_to_ref[id(expr_holder)] = ref
        return stmts, ref


@dispatch()
def convert_expr(expr_holder: ExprHolder):
    return convert_expr_op(expr_holder, expr_holder.op_node)


@dispatch()
def convert_expr(slit: SLiteral):
    ft = SIntLiteral(slit.value, convert_type(slit.hcl_type))
    Context.expr_obj_id_to_ref[id(slit)] = ft
    return [], ft


@dispatch()
def convert_expr(ulit: ULiteral):
    ft = UIntLiteral(ulit.value, convert_type(ulit.hcl_type))
    Context.expr_obj_id_to_ref[id(ulit)] = ft
    return [], ft


@dispatch()
def convert_expr(wire: Wire):
    name = NameGetter.get(wire.id)
    typ = convert_type(wire.hcl_type)

    stmt = DefWire(name, typ)
    ref = Reference(name, typ)
    Context.expr_obj_id_to_ref[id(wire)] = ref
    return [stmt], ref


@dispatch()
def convert_expr(mi: ModuleInst):
    if mi.module_name not in Context.modules:
        from py_hcl.convertor.conv_module import convert_module
        convert_module(mi.packed_module)
    module = Context.modules[mi.module_name]
    name = NameGetter.get(mi.id)
    ref = Reference(name, ports_to_bundle_type(module.ports))
    stmts = [DefInstance(name, mi.module_name),
             Connect(SubField(ref, 'clock', ClockType()),
                     Reference('clock', ClockType())),
             Connect(SubField(ref, 'reset', UIntType(Width(1))),
                     Reference('reset', UIntType(Width(1))))]
    Context.expr_obj_id_to_ref[id(mi)] = ref
    return stmts, ref


class NameGetter(object):
    cnt = -1

    @classmethod
    def get(cls, expr_id: int):
        try:
            return Context.expr_id_to_name[expr_id]
        except KeyError:
            cls.cnt += 1
            return "_T_" + str(cls.cnt)


def save_node_ref(op_ir, name, tpe, obj_id):
    stmt = DefNode(name, op_ir)
    ref = Reference(name, tpe)
    Context.expr_obj_id_to_ref[obj_id] = ref
    return stmt, ref
