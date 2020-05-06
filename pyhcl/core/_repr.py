from dataclasses import dataclass, field
from typing import Union

from pyhcl.core._dynamic_ctx import DynamicContext
from pyhcl.core._emit_context import EmitterContext
from pyhcl.core._interface import VecOps
from pyhcl.core._utils import get_attr, has_attr
from pyhcl.dsl.funcs import OneDimensionalization
from pyhcl.ir import low_ir
from pyhcl.ir import low_prim


class Node:
    """
    inner node
    """

    def __post_init__(self):
        self.scopeId = DynamicContext.currentScope()

    def __ilshift__(self, other):
        connect = Connect(self, other)
        DynamicContext.push(connect)
        return self

    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(self, other)

    def __xor__(self, other):
        return Xor(self, other)

    def __add__(self, other):
        return Add(self, other)

    def __sub__(self, other):
        return Sub(self, other)

    def __mul__(self, other):
        return Mul(self, other)

    def __truediv__(self, other):
        return Div(self, other)

    def __mod__(self, other):
        return Mod(self, other)

    def __lshift__(self, other):
        return LShift(self, other)

    def __rshift__(self, other):
        return RShift(self, other)

    def __gt__(self, other):
        return GT(self, other)

    def __le__(self, other):
        return LE(self, other)

    def __lt__(self, other):
        return LT(self, other)

    def __ge__(self, other):
        return GE(self, other)

    def __invert__(self):
        return Not(self)

    def __neg__(self):
        return Neg(self)

    def __eq__(self, other):
        from pyhcl.dsl.infra import BitPat
        if isinstance(self, BitPat):
            return self.eqFor(other)
        elif isinstance(other, BitPat):
            return other.eqFor(self)
        else:
            return Eq(self, other)

    def __ne__(self, other):
        return Neq(self, other)

    def __getitem__(self, item):
        return Index(self, item)

    def __setitem__(self, key, value):
        return self

    def __hash__(self):
        return hash(id(self))

    def to_bool(self):
        from pyhcl.dsl.cdatatype import INT
        if isinstance(self.typ, INT) or issubclass(self.typ, INT):
            return self[0]
        else:
            raise Exception("need bits type")

    def to_sint(self):
        return AsSInt(self)

    def to_uint(self):
        return AsUInt(self)

    def extractForName(self):
        return self


def _primMap(ctx: EmitterContext, obj, op, args, consts, tranFormFunc):
    if consts is None:
        consts = []

    # get items' reference and do checking
    ars = [ctx.getRef(a) for a in args]
    newArgs, typ = tranFormFunc(*ars)

    e = low_ir.DoPrim(op, newArgs, consts, typ)
    name = ctx.getName(obj)
    node = low_ir.DefNode(name, e)
    ctx.appendFinalStatement(node, obj.scopeId)
    ref = low_ir.Reference(name, typ)
    ctx.updateRef(obj, ref)
    return ref


def _pickWidth(l, r, func):
    if l.width is None:
        return r
    elif r.width is None:
        return l
    else:
        return low_ir.IntWidth(func(l.width, r.width))


def _biSameType(uintWidthFunc, sintWidthFunc):
    def _tf(lref, rref):
        if isinstance(lref.typ, low_ir.UIntType) and isinstance(rref.typ, low_ir.UIntType):
            return [lref, rref], low_ir.UIntType(_pickWidth(lref.typ.width, rref.typ.width, uintWidthFunc))
        elif isinstance(lref.typ, low_ir.SIntType) and isinstance(rref.typ, low_ir.SIntType):
            return [lref, rref], low_ir.SIntType(_pickWidth(lref.typ.width, rref.typ.width, sintWidthFunc))
        else:
            raise Exception("need uint types or sint types")

    return _tf


def _biSameTypeToBit():
    def _tf(lref, rref):
        if isinstance(lref.typ, low_ir.UIntType) and isinstance(rref.typ, low_ir.UIntType):
            return [lref, rref], low_ir.UIntType(low_ir.IntWidth(1))
        elif isinstance(lref.typ, low_ir.SIntType) and isinstance(rref.typ, low_ir.SIntType):
            return [lref, rref], low_ir.SIntType(low_ir.IntWidth(1))
        else:
            raise Exception("need uint types or sint types")

    return _tf


def _uintType(uintWidthFunc):
    def _tf(lref, rref):
        if isinstance(lref.typ, low_ir.UIntType) and isinstance(rref.typ, low_ir.UIntType):
            return [lref, rref], low_ir.UIntType(_pickWidth(lref.typ.width, rref.typ.width, uintWidthFunc))
        else:
            raise Exception("need uint types")

    return _tf


@dataclass(eq=False)
class Not(Node):
    item: Node

    def __post_init__(self):
        super().__post_init__()
        self.typ = self.item.typ

    @staticmethod
    def _tf(ref):
        if isinstance(ref.typ, low_ir.UIntType):
            return [ref], ref.typ
        else:
            raise Exception("need uint type")

    def mapToIR(self, ctx: EmitterContext):
        return _primMap(ctx, self, low_prim.Not(), [self.item], [], Not._tf)


@dataclass(eq=False)
class Neg(Node):
    item: Node

    def __post_init__(self):
        super().__post_init__()
        self.typ = self.item.typ

    @staticmethod
    def _tf(ref):
        if isinstance(ref.typ, low_ir.SIntType):
            return [ref], ref.typ
        else:
            raise Exception("need sint type")

    def mapToIR(self, ctx: EmitterContext):
        return _primMap(ctx, self, low_prim.Neg(), [self.item], [], Neg._tf)


@dataclass(eq=False)
class And(Node):
    lhs: Node
    rhs: Node

    def __post_init__(self):
        super().__post_init__()
        self.typ = self.lhs.typ

    def mapToIR(self, ctx: EmitterContext):
        return _primMap(ctx, self, low_prim.And(), [self.lhs, self.rhs], [], _uintType(lambda x, y: max(x, y)))


@dataclass(eq=False)
class Or(Node):
    lhs: Node
    rhs: Node

    def __post_init__(self):
        super().__post_init__()
        self.typ = self.lhs.typ

    def mapToIR(self, ctx: EmitterContext):
        return _primMap(ctx, self, low_prim.Or(), [self.lhs, self.rhs], [], _uintType(lambda x, y: max(x, y)))


@dataclass(eq=False)
class Xor(Node):
    lhs: Node
    rhs: Node

    def __post_init__(self):
        super().__post_init__()
        self.typ = self.lhs.typ

    def mapToIR(self, ctx: EmitterContext):
        return _primMap(ctx, self, low_prim.Xor(), [self.lhs, self.rhs], [], _uintType(lambda x, y: max(x, y)))


@dataclass(eq=False)
class Add(Node):
    lhs: Node
    rhs: Node

    def __post_init__(self):
        super().__post_init__()
        self.typ = self.lhs.typ

    def mapToIR(self, ctx: EmitterContext):
        return _primMap(ctx, self,
                        low_prim.Add(),
                        [self.lhs, self.rhs],
                        [],
                        _biSameType(lambda x, y: max(x, y),
                                    lambda x, y: max(x, y) + 1))


@dataclass(eq=False)
class Sub(Node):
    lhs: Node
    rhs: Node

    def __post_init__(self):
        super().__post_init__()
        self.typ = self.lhs.typ

    def mapToIR(self, ctx: EmitterContext):
        return _primMap(ctx, self,
                        low_prim.Sub(),
                        [self.lhs, self.rhs],
                        [],
                        _biSameType(lambda x, y: max(x, y),
                                    lambda x, y: max(x, y) + 1))


@dataclass(eq=False)
class Mul(Node):
    lhs: Node
    rhs: Node

    def __post_init__(self):
        super().__post_init__()
        self.typ = self.lhs.typ

    def mapToIR(self, ctx: EmitterContext):
        return _primMap(ctx, self,
                        low_prim.Mul(),
                        [self.lhs, self.rhs],
                        [],
                        _biSameType(lambda x, y: x + y,
                                    lambda x, y: x + y))


@dataclass(eq=False)
class Div(Node):
    lhs: Node
    rhs: Node

    def __post_init__(self):
        super().__post_init__()
        self.typ = self.lhs.typ

    def mapToIR(self, ctx: EmitterContext):
        return _primMap(ctx, self,
                        low_prim.Div(),
                        [self.lhs, self.rhs],
                        [],
                        _biSameType(lambda x, y: x,
                                    lambda x, y: x))


@dataclass(eq=False)
class Mod(Node):
    lhs: Node
    rhs: Node

    def __post_init__(self):
        super().__post_init__()
        self.typ = self.lhs.typ

    def mapToIR(self, ctx: EmitterContext):
        return _primMap(ctx, self,
                        low_prim.Rem(),
                        [self.lhs, self.rhs],
                        [],
                        _biSameType(lambda x, y: y,
                                    lambda x, y: y))


@dataclass(eq=False)
class LShift(Node):
    lhs: Node
    rhs: Node

    def __post_init__(self):
        super().__post_init__()
        self.typ = self.lhs.typ

    @staticmethod
    def _shltf(lref, n):
        if isinstance(lref.typ, low_ir.UIntType):
            return [lref], low_ir.UIntType(_pickWidth(lref.typ.width, low_ir.IntWidth(n), lambda x, y: x + y))
        elif isinstance(lref.typ, low_ir.SIntType):
            return [lref], low_ir.SIntType(_pickWidth(lref.typ.width, low_ir.IntWidth(n), lambda x, y: x + y))
        else:
            raise Exception("need uint type or sint type")

    @staticmethod
    def _dshltf(lref, rref):
        if isinstance(lref.typ, low_ir.UIntType) and isinstance(rref.typ, low_ir.UIntType):
            return [lref, rref], low_ir.UIntType(
                _pickWidth(lref.typ.width, rref.typ.width, lambda x, y: x + (1 << y) - 1))
        elif isinstance(lref.typ, low_ir.SIntType) and isinstance(rref.typ, low_ir.UIntType):
            return [lref, rref], low_ir.SIntType(
                _pickWidth(lref.typ.width, rref.typ.width, lambda x, y: x + (1 << y) - 1))
        else:
            raise Exception("lhs needs uint type or sint type, rhs needs uint type")

    def mapToIR(self, ctx: EmitterContext):
        if isinstance(self.rhs, int):
            return _primMap(ctx, self, low_prim.Shl(), [self.lhs], [self.rhs], lambda x: LShift._shltf(x, self.rhs))
        else:
            return _primMap(ctx, self, low_prim.Dshl(), [self.lhs, self.rhs], [], LShift._dshltf)


@dataclass(eq=False)
class RShift(Node):
    lhs: Node
    rhs: Node

    def __post_init__(self):
        super().__post_init__()
        self.typ = self.lhs.typ

    @staticmethod
    def _shrtf(lref, n):
        if isinstance(lref.typ, low_ir.UIntType):
            return [lref], low_ir.UIntType(_pickWidth(lref.typ.width, low_ir.IntWidth(n), lambda x, y: x - y))
        elif isinstance(lref.typ, low_ir.SIntType):
            return [lref], low_ir.SIntType(_pickWidth(lref.typ.width, low_ir.IntWidth(n), lambda x, y: x - y))
        else:
            raise Exception("need uint type or sint type")

    @staticmethod
    def _dshltf(lref, rref):
        if isinstance(lref.typ, low_ir.UIntType) and isinstance(rref.typ, low_ir.UIntType):
            return [lref, rref], lref.typ
        elif isinstance(lref.typ, low_ir.SIntType) and isinstance(rref.typ, low_ir.UIntType):
            return [lref, rref], lref.typ
        else:
            raise Exception("lhs needs uint type or sint type, rhs needs uint type")

    def mapToIR(self, ctx: EmitterContext):
        if isinstance(self.rhs, int):
            return _primMap(ctx, self, low_prim.Shr(), [self.lhs], [self.rhs], lambda x: RShift._shrtf(x, self.rhs))
        else:
            return _primMap(ctx, self, low_prim.Dshr(), [self.lhs, self.rhs], [], RShift._dshltf)


@dataclass(eq=False)
class GT(Node):
    lhs: Node
    rhs: Node

    def __post_init__(self):
        super().__post_init__()
        from pyhcl.dsl.cdatatype import Bool
        self.typ = Bool

    def mapToIR(self, ctx: EmitterContext):
        return _primMap(ctx, self, low_prim.Gt(), [self.lhs, self.rhs], [], _biSameTypeToBit())


@dataclass(eq=False)
class GE(Node):
    lhs: Node
    rhs: Node

    def __post_init__(self):
        super().__post_init__()
        from pyhcl.dsl.cdatatype import Bool
        self.typ = Bool

    def mapToIR(self, ctx: EmitterContext):
        return _primMap(ctx, self, low_prim.Geq(), [self.lhs, self.rhs], [], _biSameTypeToBit())


@dataclass(eq=False)
class LT(Node):
    lhs: Node
    rhs: Node

    def __post_init__(self):
        super().__post_init__()
        from pyhcl.dsl.cdatatype import Bool
        self.typ = Bool

    def mapToIR(self, ctx: EmitterContext):
        return _primMap(ctx, self, low_prim.Lt(), [self.lhs, self.rhs], [], _biSameTypeToBit())


@dataclass(eq=False)
class LE(Node):
    lhs: Node
    rhs: Node

    def __post_init__(self):
        super().__post_init__()
        from pyhcl.dsl.cdatatype import Bool
        self.typ = Bool

    def mapToIR(self, ctx: EmitterContext):
        return _primMap(ctx, self, low_prim.Leq(), [self.lhs, self.rhs], [], _biSameTypeToBit())


@dataclass(eq=False)
class Eq(Node):
    lhs: Node
    rhs: Node

    def __post_init__(self):
        super().__post_init__()
        from pyhcl.dsl.cdatatype import Bool
        self.typ = Bool

    def mapToIR(self, ctx: EmitterContext):
        return _primMap(ctx, self, low_prim.Eq(), [self.lhs, self.rhs], [], _biSameTypeToBit())


@dataclass(eq=False)
class Neq(Node):
    lhs: Node
    rhs: Node

    def __post_init__(self):
        super().__post_init__()
        from pyhcl.dsl.cdatatype import Bool
        self.typ = Bool

    def mapToIR(self, ctx: EmitterContext):
        return _primMap(ctx, self, low_prim.Neq(), [self.lhs, self.rhs], [], _biSameTypeToBit())


@dataclass(eq=False)
class Cat(Node):
    lhs: Node
    rhs: Node

    def __post_init__(self):
        super().__post_init__()
        self.typ = self.lhs.typ

    def mapToIR(self, ctx: EmitterContext):
        return _primMap(ctx, self, low_prim.Cat(), [self.lhs, self.rhs], [], _uintType(lambda x, y: x + y))


@dataclass(eq=False)
class AsUInt(Node):
    item: Node

    def __post_init__(self):
        super().__post_init__()
        from pyhcl.dsl.cdatatype import U
        self.typ = U.w()

    @staticmethod
    def _tf(ref):
        if isinstance(ref.typ, low_ir.UIntType):
            return [ref], ref.typ
        elif isinstance(ref.typ, low_ir.SIntType):
            return [ref], low_ir.UIntType(ref.typ.width)
        else:
            Exception("need sint type")

    def mapToIR(self, ctx: EmitterContext):
        return _primMap(ctx, self, low_prim.AsUInt(), [self.item], [], AsUInt._tf)


@dataclass(eq=False)
class AsSInt(Node):
    item: Node

    def __post_init__(self):
        super().__post_init__()
        from pyhcl.dsl.cdatatype import S
        self.typ = S.w()

    @staticmethod
    def _tf(ref):
        if isinstance(ref.typ, low_ir.UIntType):
            return [ref], low_ir.SIntType(ref.typ.width)
        elif isinstance(ref.typ, low_ir.SIntType):
            return [ref], ref.typ
        else:
            Exception("need uint type")

    def mapToIR(self, ctx: EmitterContext):
        return _primMap(ctx, self, low_prim.AsSInt(), [self.item], [], AsSInt._tf)


class CType(Node):
    def mapToIR(self, ctx: EmitterContext):
        return low_ir.UnknownType()


@dataclass(eq=False)
class VecView(VecOps, CType):
    ref: Node
    typ: "Vec"

    def provideVector(self):
        return True, self.typ


class ReverseView(VecView):
    def indexTransform(self, index):
        from pyhcl.dsl.cdatatype import U
        if isinstance(index, int):
            idx = self.typ.size - index - 1
        else:
            idx = U(self.typ.size - 1) - index

        tf = get_attr(self.ref, "indexTransform")
        if tf is not None:
            newIndex = tf(idx)
        else:
            newIndex = Index(self.ref, idx)

        return newIndex


@dataclass(eq=False)
class FlattenView(VecView):
    l0: int
    l1: int

    def indexTransform(self, index):
        from pyhcl.dsl.cdatatype import U
        if isinstance(index, int):
            l0i = index // self.l1
            l1i = index % self.l1
        else:
            l0i = index / U(self.l1)
            l1i = index % U(self.l1)

        tf = get_attr(self.ref, "indexTransform")
        if tf is not None:
            newIndex = Index(tf(l0i), l1i)
        else:
            newIndex = Index(Index(self.ref, l0i), l1i)

        return newIndex


@dataclass(eq=False)
class Index(VecOps, Node):
    ref: Node
    index: Union[int, slice, CType]
    typ: CType = field(default=None, init=False)

    def __post_init__(self):
        from pyhcl.dsl.vector import Vec
        super().__post_init__()
        if isinstance(self.ref.typ, Vec):
            # for iterating vector type
            if isinstance(self.index, slice):
                self.typ = self.ref.typ
                start = 0 if self.index.start is None else self.index.start
                stop = self.typ.size if self.index.stop is None else self.index.stop
                step = 1 if self.index.step is None else self.index.step
                self.index = slice(start, stop, step)
            else:
                self.typ = self.ref.typ.typ
        else:
            self.typ = self.ref.typ.getIndexedType()

    def __iter__(self):
        from pyhcl.dsl.vector import Vec
        if isinstance(self.typ, Vec) and isinstance(self.index, slice):
            return iter(self.ref[i] for i in range(self.index.start, self.index.stop, self.index.step))
        else:
            return super().__iter__()

    def mapToIR(self, ctx: EmitterContext):
        newIndex = self._transform()
        return self._doMap(ctx, newIndex.index, newIndex.ref)

    def _transform(self):
        if has_attr(self.ref, "indexTransform"):
            index = get_attr(self.ref, "indexTransform")(self.index)
        else:
            index = self
        return index

    def _doMap(self, ctx, idx, ref):
        rf = ctx.getRef(ref)

        if isinstance(idx, Node):
            idx = ctx.getRef(idx)

        v = rf.typ.irWithIndex(idx)(rf)
        ir = v["ir"]
        if "inNode" in v:
            # ground type
            name = ctx.getName(self)
            node = low_ir.DefNode(name, ir)
            ctx.appendFinalStatement(node, self.scopeId)
            ref = low_ir.Reference(name, ir.typ)
            ctx.updateRef(self, ref)
            return ref
        elif "inPort" in v:
            # memory type
            name = ctx.getName(self)
            memPort = ir(name, rf, ctx.getClock(), self._mem_rw if has_attr(self, "_mem_rw") else True)
            ctx.appendFinalStatement(memPort, self.scopeId)
            ref = low_ir.Reference(name, rf.typ.typ)
            ctx.updateRef(self, ref)
            return ref
        else:
            return ir


class Declare:
    def __post_init__(self):
        self.scopeId = DynamicContext.currentScope()


@dataclass(eq=False)
class Connect(Declare):
    lhs: Node
    rhs: Node

    def __post_init__(self):
        super().__post_init__()
        self.lhs._mem_rw = False

    def mapToIR(self, ctx: EmitterContext):
        from pyhcl.dsl.vector import Vec

        if has_attr(self.lhs, "typ") and has_attr(self.rhs, "typ") \
                and (isinstance(self.lhs.typ, Vec) or isinstance(self.rhs.typ, Vec)):
            lhs = OneDimensionalization(self.lhs)
            rhs = OneDimensionalization(self.rhs)

            if len(lhs) != len(rhs):
                raise Exception("vector size does not match")

            for l, r in zip(lhs, rhs):
                Connect._doConnect(ctx, l.mapToIR(ctx), r.mapToIR(ctx), self.scopeId)
        else:
            Connect._doConnect(ctx, ctx.getRef(self.lhs), ctx.getRef(self.rhs), self.scopeId)

    @staticmethod
    def _doConnect(ctx, lref, rref, scopeId):
        if isinstance(lref.typ, low_ir.UIntType) and isinstance(rref.typ, low_ir.UIntType):
            if lref.typ.width.width is not None and rref.typ.width.width is not None:
                if lref.typ.width.width >= rref.typ.width.width:
                    Connect._unsafeConnect(lref, rref, ctx, scopeId)
                else:
                    bits = low_ir.DoPrim(low_ir.Bits(), [rref], [lref.typ.width.width - 1, 0], lref.typ)
                    Connect._unsafeConnect(lref, bits, ctx, scopeId)
            else:
                Connect._unsafeConnect(lref, rref, ctx, scopeId)
        elif isinstance(lref.typ, low_ir.SIntType) and isinstance(rref.typ, low_ir.SIntType):
            if lref.typ.width.width is not None and rref.typ.width.width is not None:
                if lref.typ.width.width >= rref.typ.width.width:
                    Connect._unsafeConnect(lref, rref, ctx, scopeId)
                else:
                    bits = low_ir.DoPrim(low_ir.Bits(), [rref], [lref.typ.width.width - 1, 0], lref.typ)
                    Connect._unsafeConnect(lref, bits, ctx, scopeId)
            else:
                Connect._unsafeConnect(lref, rref, ctx, scopeId)
        else:
            raise Exception("type does not match")

    @staticmethod
    def _unsafeConnect(lref, rref, ctx, scopeId):
        c = low_ir.Connect(lref, rref)
        ctx.appendFinalStatement(c, scopeId)


@dataclass(eq=False)
class MemType(CType):
    size: int
    typ: CType

    def getIndexedType(self):
        return self.typ

    def mapToIR(self, ctx: EmitterContext):
        return low_ir.MemoryType(self.typ.mapToIR(ctx), self.size)


class SubField(VecOps, Node):
    def __init__(self, value, name, ref):
        self.value = value
        self.name = name
        self.ref = ref
        self.typ = value.typ

    def __getattribute__(self, item):
        res = get_attr(self, item)
        if res is not None:
            return res

        value = get_attr(self, "value")
        obj = getattr(value, item)

        whiteList = {"typ", "lvl", "scopeId"}

        if item in whiteList:
            return obj
        elif isinstance(obj, SubField):
            obj.ref = self
            return obj
        else:
            return SubField(obj, item, self)

    def __repr__(self):
        value = get_attr(self, "value")
        name = get_attr(self, "name")
        ref = get_attr(self, "ref")
        return "SubField(value=" + str(value) + ", name=" + str(name) + ", ref=object of " + str(
            get_attr(ref, "__class__")) + ")"

    def mapToIR(self, ctx: EmitterContext):
        ref = get_attr(self, "ref")
        name = get_attr(self, "name")
        n = ctx.getRef(ref)

        typ = next(f.typ for f in n.typ.fields if f.name == name)
        f = low_ir.SubField(n, name, typ)
        ctx.updateRef(self, f)
        return f