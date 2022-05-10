from pyhcl.ir.low_ir import *
from typing import Dict
@dataclass
class SymbolTable:
    table: Dict = {}

    def gen_typ(self, typ: Type):
        if isinstance(typ, (AsyncResetType, ResetType, ClockType, UIntType, SIntType)):
            return None
        elif isinstance(typ, VectorType):
            return [self.gen_typ(typ.typ) for _ in range(typ.size)]
        elif isinstance(typ, BundleType):
            return {f.name: self.gen_typ(f.typ) for f in typ.fields}
        elif isinstance(typ, MemoryType):
            return [self.gen_typ(typ.typ) for _ in range(typ.size)]

    def set_type(self, mname: str, name: str, t: Type):
        self.table[mname][name] = self.gen_typ(t)
    
    def has_symbol(self, mname: str, name: str) -> bool:
        return name in self.table[mname]
    
    def set_module(self, mname: str):
        self.table[mname] = {}
    
    def set_port(self, mname: str, p: Port):
        self.set_type(mname, p.name, p.typ)
    
    def set_stmt(self, mname: str, s: Statement):
        if isinstance(s, DefWire):
            self.set_type(mname, s.name, s.typ)
        elif isinstance(s, DefRegister):
            self.set_type(mname, s.name, s.typ)
        elif isinstance(s, DefMemory):
            self.set_type(mname, s.name, s.memType)
        elif isinstance(s, DefNode):
            self.set_type(mname, s.name, s.value.typ)
        elif isinstance(s, DefInstance):
            self.table[mname][s.name] = {p.name: self.gen_typ(p.typ) for p in s.ports}
        else:
            ...
    
    def get_symbol_value(self, mname: str, name: str):
        return self.table[mname][name]

    def set_symbol_value(self, mname: str, name: str, signal: int):
        self.table[mname][name] = signal
        return signal