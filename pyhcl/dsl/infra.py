from dataclasses import dataclass, field
from typing import Type, Union

from pyhcl.core._emit_context import EmitterContext
from pyhcl.core._repr import CType, Node, And, Eq
from pyhcl.core._interface import BundleAccessor, VecOps
from pyhcl.dsl.cdatatype import Bool, U
from pyhcl.ir import low_ir


@dataclass(eq=False)
class Wire(BundleAccessor, VecOps, CType):
    typ: Union[Type[CType], CType]

    def mapToIR(self, ctx: EmitterContext):
        typ = ctx.getRef(self.typ)
        name = ctx.getName(self)

        w = low_ir.DefWire(name, typ)
        ctx.appendFinalStatement(w, self.scopeId)
        ref = low_ir.Reference(name, typ)
        ctx.updateRef(self, ref)

        return ref


@dataclass(eq=False)
class RegInit(CType):
    initValue: CType
    typ: CType = field(init=False, default=None)

    def __post_init__(self):
        super().__post_init__()
        self.typ = self.initValue

    def mapToIR(self, ctx: EmitterContext):
        val = ctx.getRef(self.initValue)
        name = ctx.getName(self)

        w = low_ir.DefRegister(name, val.typ, ctx.getClock(), ctx.getReset(), val)
        ctx.appendFinalStatement(w, self.scopeId)
        ref = low_ir.Reference(name, val.typ)
        ctx.updateRef(self, ref)

        return ref


@dataclass(eq=False)
class Reg(BundleAccessor, VecOps, CType):
    typ: CType

    def mapToIR(self, ctx: EmitterContext):
        typ = self.typ.mapToIR(ctx)
        name = ctx.getName(self)

        w = low_ir.DefRegister(name, typ, ctx.getClock())
        ctx.appendFinalStatement(w, self.scopeId)
        ref = low_ir.Reference(name, typ)
        ctx.updateRef(self, ref)

        return ref


@dataclass(eq=False)
class Mux(BundleAccessor, VecOps, Node):
    cond: Node
    conseq: Node
    alt: Node
    typ: CType = field(init=False, default=None)

    def __post_init__(self):
        super().__post_init__()
        self.typ = self.conseq.typ

    def mapToIR(self, ctx: EmitterContext):
        name = ctx.getName(self)

        cond = ctx.getRef(self.cond)
        conseq = ctx.getRef(self.conseq)
        alt = ctx.getRef(self.alt)

        m = low_ir.Mux(cond, conseq, alt, conseq.typ)
        n = low_ir.DefNode(name, m)
        ctx.appendFinalStatement(n, self.scopeId)
        ref = low_ir.Reference(name, conseq.typ)
        ctx.updateRef(self, ref)

        return ref


def LookUpTable(node: Node, table: dict):
    assert len(table) > 0
    t = list(table.items())

    if t[-1][0] is not ...:
        raise Exception("should define a default value: { ...: default value }")

    i = t[-1][1]
    for n, v in t[-2::-1]:
        i = Mux(n == node, v, i)

    return i


@dataclass(eq=False)
class BitPat(Node):
    bits: str

    def __post_init__(self):
        super().__post_init__()
        self.typ = U.w(len(self.bits))
        cmp = "".join(["1" if c == "1" else "0" for c in self.bits])
        mask = "".join(["0" if c == "?" else "1" for c in self.bits])
        self.cmp = self.typ(int(cmp, 2))
        self.mask = self.typ(int(mask, 2))

    def eqFor(self, that):
        if isinstance(that, BitPat):
            return Bool(True) if self.bits == that.bits else Bool(False)
        else:
            a = And(that, self.mask)
            a.scopeId = self.scopeId
            b = Eq(a, self.cmp)
            b.scopeId = self.scopeId
            return b
