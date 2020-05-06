from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from pyhcl.core._emit_context import EmitterContext
from pyhcl.core._repr import CType, SubField
from pyhcl.core._utils import get_attr
from pyhcl.ir import low_ir


@dataclass(eq=False, init=False)
class Bundle(CType):
    _kv: Dict[str, CType]

    def __init__(self, **kwargs):
        self._kv = kwargs
        self.typ = self

    def __getattribute__(self, item):
        res = get_attr(self, item)
        if res is not None:
            return res
        else:
            return SubField(getattr(self, '_kv')[item], item, None)

    def extend(self, other: Bundle):
        kv = self._kv.copy()
        kv.update(other._kv)
        return Bundle(**kv)

    def mapToIR(self, ctx: EmitterContext):
        fs = []
        for k, v in self._kv.items():
            f = low_ir.Field(k, low_ir.Default(), v.mapToIR(ctx))
            fs.append(f)
        return low_ir.BundleType(fs)
