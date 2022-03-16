from abc import ABC
from typing import overload
from pyhcl.ir.low_ir import *

class Flow(ABC):
    ...

class SourceFlow(Flow):
    ...

class SinkFlow(Flow):
    ...

class DuplexFlow(Flow):
    ...

class UnknownFlow(Flow):
    ...

class Kind(ABC):
    ...

class PortKind(Kind):
    ...

class VarWidth(Width):
    name: str

    def serialize(self):
        return self.name