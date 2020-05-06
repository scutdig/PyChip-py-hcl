from __future__ import annotations

from dataclasses import dataclass
from typing import Type, Union, Dict

from pyhcl.core._emit_context import EmitterContext
from pyhcl.core._meta_pub import MetaPub
from pyhcl.core._repr import CType
from pyhcl.dsl.bundle import Bundle
from pyhcl.core._interface import BundleAccessor, VecOps
from pyhcl.ir import low_ir


@dataclass(init=False, eq=False)
class IO(BundleAccessor, metaclass=MetaPub):
    _ios: Dict[str, Union[Input, Output]]

    def __init__(self, **kwargs):
        self._ios = kwargs

    def provideBundle(self):
        return True, Bundle(**self._ios)

    def mapToIR(self, ctx: EmitterContext):
        name = ctx.getName(self)
        fs = []
        for k, v in self._ios.items():
            f = v.mapToIOFieldIR(k, ctx)
            fs.append(f)

        typ = low_ir.BundleType(fs)
        port = low_ir.Port(name, low_ir.Output(), low_ir.BundleType(fs))
        ref = low_ir.Reference(name, typ)
        ctx.updateRef(self, ref)
        ctx.appendFinalPort(port)
        return ref


@dataclass(eq=False)
class Input(BundleAccessor, VecOps, CType, metaclass=MetaPub):
    typ: Union[CType, Type[CType]]

    def mapToIR(self, ctx: EmitterContext):
        return _mapToIR(self, ctx, low_ir.Input())

    def mapToIOFieldIR(self, name: str, ctx: EmitterContext):
        ir = self.typ.mapToIR(ctx)
        f = low_ir.Field(name, low_ir.Flip(), ir)
        return f


@dataclass(eq=False)
class Output(BundleAccessor, VecOps, CType, metaclass=MetaPub):
    typ: Union[CType, Type[CType]]

    def mapToIR(self, ctx: EmitterContext):
        return _mapToIR(self, ctx, low_ir.Output())

    def mapToIOFieldIR(self, name: str, ctx: EmitterContext):
        ir = self.typ.mapToIR(ctx)
        f = low_ir.Field(name, low_ir.Default(), ir)
        return f


def _mapToIR(io, ctx, lowIR):
    name = ctx.getName(io)
    typ = io.typ.mapToIR(ctx)
    port = low_ir.Port(name, lowIR, typ)
    ref = low_ir.Reference(name, typ)
    ctx.updateRef(io, ref)
    ctx.appendFinalPort(port)
    return ref
