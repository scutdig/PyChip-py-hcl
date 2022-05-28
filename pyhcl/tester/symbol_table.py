from pyhcl.ir.low_ir import *

@dataclass(frozen=True)
class SymbolTable:
    table = {}
    clock_table = {}

    def gen_typ(self, typ: Type):
        if isinstance(typ, (AsyncResetType, ResetType, ClockType, UIntType, SIntType)):
            return 0
        elif isinstance(typ, VectorType):
            return [self.gen_typ(typ.typ) for _ in range(typ.size)]
        elif isinstance(typ, BundleType):
            return {f.name: self.gen_typ(f.typ) for f in typ.fields}
        elif isinstance(typ, MemoryType):
            return [self.gen_typ(typ.typ) for _ in range(typ.size)]

    def has_symbol(self, mname: str, name: str) -> bool:
        return name in self.table[mname]
    
    def set_module(self, mname: str):
        self.table[mname] = {}
    
    def set_symbol(self, mname: str, symbol):
        if isinstance(symbol, Port):
            if isinstance(symbol.typ, ClockType):
                self.clock_table[mname][symbol.name] = self.gen_typ(symbol.typ)
            self.table[mname][symbol.name] = self.gen_typ(symbol.typ)
        if isinstance(symbol, DefWire):
            self.table[mname][symbol.name] = self.gen_typ(symbol.typ)
        elif isinstance(symbol, DefRegister):
            self.table[mname][symbol.name] = self.gen_typ(symbol.typ)
        elif isinstance(symbol, DefMemory):
            self.table[mname][symbol.name] = self.gen_typ(symbol.memType)
        elif isinstance(symbol, DefNode):
            self.table[mname][symbol.name] = self.gen_typ(symbol.value.typ)
        elif isinstance(symbol, DefInstance):
            self.table[mname][symbol.name] = {p.name: self.gen_typ(p.typ) for p in symbol.ports}
        else:
            ...
    
    def get_symbol_value(self, mname: str, names: list, table = None):
        if table is None:
            table = self.table[mname]
        ns = names[:]
        while len(ns) > 1:
            table = table[ns.pop()]
        return table[ns.pop()]

    def set_symbol_value(self, mname: str, names: list, signal: int, table = None):
        if table is None:
            table = self.table[mname]
        ns = names[:]
        while len(ns) > 1:
            table = table[ns.pop()]
        table[ns.pop()] = signal
        return signal