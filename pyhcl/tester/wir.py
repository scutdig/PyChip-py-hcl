from pyclbr import Function
from pyhcl.ir.low_ir import *
@dataclass(frozen=True)
class WUIntLiteral(Expression):
    expr: Expression

    def get_value(self, *args) -> int:
        return self.expr.value
    
    def serialize(self) -> str:
        ...
    
    def verilog_serialize(self) -> str:
        ...

@dataclass(frozen=True)
class WSIntLiteral(Expression):
    expr: Expression

    def get_value(self, *args) -> int:
        return self.expr.value
    
    def serialize(self) -> str:
        ...
    
    def verilog_serialize(self) -> str:
        ...

@dataclass(frozen=True)
class WReference(Expression):
    expr: Expression
    get_func: Function
    set_func: Function

    def get_value(self, *args) -> int:
        return self.get_func(*args)
    
    def set_value(self, *args) -> int:
        return self.set_func(*args)

    def serialize(self) -> str:
        ...

    def verilog_serialize(self) -> str:
        ...

@dataclass(frozen=True)
class WSubField(Expression):
    expr: Expression
    get_func: Function
    set_func: Function

    def get_value(self, *args) -> int:
        return self.get_func(*args)
    
    def set_value(self, *args) -> int:
        return self.set_func(*args)
    
    def serialize(self) -> str:
        ...

    def verilog_serialize(self) -> str:
        ...

@dataclass(frozen=True)
class WSubIndex(Expression):
    expr: Expression
    get_func: Function
    set_func: Function

    def get_value(self, *args) -> int:
        return self.get_func(*args)
    
    def set_value(self, *args) -> int:
        return self.set_func(*args)
    
    def serialize(self) -> str:
        ...
    
    def verilog_serialize(self) -> str:
        ...

@dataclass(frozen=True)
class WSubAccess(Expression):
    expr: Expression
    get_func: Function
    set_func: Function

    def get_value(self, *args) -> int:
        return self.get_func(*args)
    
    def set_value(self, *args) -> int:
        return self.set_func(*args)
    
    def serialize(self) -> str:
        ...
    
    def verilog_serialize(self) -> str:
        ...

@dataclass(frozen=True)
class WMux(Expression):
    expr: Expression
    get_func: Function

    def get_value(self, *args) -> int:
        return self.get_func(*args)
    
    def serialize(self) -> str:
        ...
    
    def verilog_serialize(self) -> str:
        ...

@dataclass(frozen=True)
class WValidIf(Expression):
    expr: Expression
    get_func: Function

    def get_value(self, *args) -> int:
        return self.get_func(*args)
    
    def serialize(self) -> str:
        ...
    
    def verilog_serialize(self) -> str:
        ...

@dataclass(frozen=True)
class WDoPrim(Expression):
    expr: Expression
    get_func: Function

    def get_value(self, *args) -> int:
        return self.get_func(*args)
    
    def serialize(self) -> str:
        ...
    
    def verilog_serialize(self) -> str:
        ...

@dataclass(frozen=True)
class WInt(Expression):
    value: int

    def get_value(self, *args) -> int:
        return self.value
    
    def serialize(self) -> str:
        ...
    
    def verilog_serialize(self) -> str:
        ...