from abc import ABC
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

class WrappedType(Type):
    def __init__(self, t: Type):
        self.t = t

    def __eq__(self, o):
        if isinstance(o, WrappedType):
            return WrappedType.compare(self.t, o.t)
        else:
            return False
    
    @staticmethod
    def compare(sink: Type, source: Type):
        def legal_reset_type(self, typ: Type) -> bool:
            if isinstance(typ, UIntType) and isinstance(typ.width, IntWidth):
                return typ.width.width == 1
            elif isinstance(typ, AsyncResetType):
                return True
            elif isinstance(typ, ResetType):
                return True
            else:
                return False

        if isinstance(sink, UIntType) and isinstance(source, UIntType):
            return True
        elif isinstance(sink, SIntType) and isinstance(source, SIntType):
            return True
        elif isinstance(sink, ClockType) and isinstance(source, ClockType):
            return True
        elif isinstance(sink, AsyncResetType) and isinstance(source, AsyncResetType):
            return True
        elif isinstance(sink, ResetType):
            return legal_reset_type(source)
        elif isinstance(source, ResetType):
            return legal_reset_type(sink)
        elif isinstance(sink, VectorType) and isinstance(source, VectorType):
            return sink.size == source.size and WrappedType.compare(sink.typ, source.typ)
        elif isinstance(sink, BundleType) and isinstance(source, BundleType):
            final = True
            for f1, f2 in list(zip(sink.fields, source.fields)):
                f1_final = WrappedType.compare(f2.typ, f1.typ) if isinstance(f1.flip, Flip) else WrappedType.compare(f1.typ, f2.typ)
                final = f1.flip == f2.flip and f1.name == f2.name and f1_final and final
            
            return len(sink.fields) == len(source.fields) and final
        else:
            return False
    
    def serialize(self) -> str:
        ...
    
    def verilog_serialize(self) -> str:
        ...