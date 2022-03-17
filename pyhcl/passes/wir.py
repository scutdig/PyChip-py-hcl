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
    t: Type

    def __eq__(self, o):
        if type(o) == WrappedType:
            return WrappedType.compare(self.t, o.t)
        else:
            return False
    
    @staticmethod
    def compare(sink: Type, source: Type):
        def legal_reset_type(self, typ: Type) -> bool:
            if type(typ) == UIntType and type(typ.width) == IntWidth:
                return typ.width.width == 1
            elif type(typ) == AsyncResetType:
                return True
            elif type(typ) == ResetType:
                return True
            else:
                return False

        if type(sink) == UIntType and type(source) == UIntType:
            return True
        elif type(sink) == SIntType and type(source) == SIntType:
            return True
        elif type(sink) == ClockType and type(source) == ClockType:
            return True
        elif type(sink) == AsyncResetType and type(source) == AsyncResetType:
            return True
        elif type(sink) == ResetType:
            return legal_reset_type(source)
        elif type(source) == ResetType:
            return legal_reset_type(sink)
        elif type(sink) == VectorType and type(source) == VectorType:
            return sink.size == source.size and WrappedType.compare(sink.typ, source.typ)
        elif type(sink) == BundleType and type(source) == BundleType:
            final = True
            for f1, f2 in list(zip(sink.fields, source.fields)):
                f1_final = WrappedType.compare(f2.typ, f1.typ) if type(f1.flip) == Flip else WrappedType.compare(f1.typ, f2.typ)
                final = f1.flip == f2.flip and f1.name == f2.name and f1_final and final
            
            return len(sink.fields) == len(source.fields) and final
        else:
            return False