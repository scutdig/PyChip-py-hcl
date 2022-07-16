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
        self.clock_table[mname] = {}
    
    def set_symbol(self, mname: str, symbol):
        if isinstance(symbol, Port):
            if isinstance(symbol.typ, ClockType):
                self.clock_table[mname][symbol.name] = self.gen_typ(symbol.typ)
            self.table[mname][symbol.name] = self.gen_typ(symbol.typ)
        if isinstance(symbol, DefWire):
            self.table[mname][symbol.name] = self.gen_typ(symbol.typ)
        elif isinstance(symbol, DefRegister):
            self.table[mname][symbol.name] = self.gen_typ(symbol.typ)
        elif isinstance(symbol, WDefMemory):
            self.table[mname][symbol.name] = self.gen_typ(symbol.memType)
            for rw in symbol.writers:
                self.table[mname][f"{symbol.name}_{rw}_data"] = self.gen_typ(symbol.dataType)
                self.table[mname][f"{symbol.name}_{rw}_addr"] = self.gen_typ(UIntType(IntWidth(get_binary_width(symbol.depth))))
                self.table[mname][f"{symbol.name}_{rw}_clk"] = self.gen_typ(ClockType())
                self.table[mname][f"{symbol.name}_{rw}_en"] = self.gen_typ(UIntType(IntWidth(1)))
                self.table[mname][f"{symbol.name}_{rw}_mask"] = self.gen_typ(UIntType(IntWidth(1)))
            
            for rr in symbol.readers:
                self.table[mname][f"{symbol.name}_{rr}_data"] = self.gen_typ(symbol.dataType)
                self.table[mname][f"{symbol.name}_{rr}_addr"] = self.gen_typ(UIntType(IntWidth(get_binary_width(symbol.depth))))
                self.table[mname][f"{symbol.name}_{rr}_clk"] = self.gen_typ(ClockType())
                self.table[mname][f"{symbol.name}_{rr}_en"] = self.gen_typ(UIntType(IntWidth(1)))
        elif isinstance(symbol, DefNode):
            self.table[mname][symbol.name] = self.gen_typ(symbol.value.typ)
        elif isinstance(symbol, DefInstance):
            for p in symbol.ports:
                name = f"{symbol.name}_{p.name}"
                self.table[mname][name] = self.gen_typ(p.typ)
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