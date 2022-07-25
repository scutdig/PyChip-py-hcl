# Other Features

## Utils
### General
### Cloneing hardware datatypes
### Passing a datatype as constructions parameter
#### The old way
#### The safe way
### Frequency and time
### Binary prefix


## Stub


## Assertions


## Report


## ScopeProperty


## Analog and inout
### Introduction
### Analog
### inout
### InOutWrapper
### Manually driving Analog bundles


## VHDL and Verilog generation
### Generate VHDL and Verilog from a SpinalHDL Component
#### Parametrization from Scala
#### Parametrization from shell
### Generated VHDL and Verilog
#### Organization
#### Combinational logic
#### Sequential logic
### VHDL and Verilog attributes


## Introduction
### Introduction


























## Pysv


```python
import random

from pyhcl import *
from pysv import sv, DataType, Reference
from pyhcl.simulator import Simlite, DpiConfig
import random

class Add(BlackBox):
    io = IO(
        in1=Input(U.w(32)),
        out=Output(U.w(32))
    )


@sv(a=DataType.UInt, return_type=Reference(x=DataType.UInt))
def fn(a):
    return a + 10000


addpysvmodule(Add, fn)

class Rand(BlackBox):
    io = IO(
        in1=Input(U.w(32)),
        in2=Input(U.w(32)),
        out=Output(U.w(32))
    )


@sv(a=DataType.UInt, b=DataType.UInt, return_type=Reference(x=DataType.UInt))
def fn2(a, b):
    return random.randint(a, b)


addpysvmodule(Rand, fn2)
compile_and_binding_all()


class Top(Module):
    io = IO(
        a=Input(U.w(32)),
        b=Input(U.w(32)),
        c=Output(U.w(32))
    )

    wire = Wire(U.w(32))

    r = Rand()
    add = Add()
    r.io.in1 @= io.a
    r.io.in2 @= io.b
    wire @= r.io.out
    add.io.in1 @= wire
    io.c @= add.io.out



if __name__ == '__main__':
    cfg = DpiConfig()
    # Emitter.dumpVerilog(Emitter.dump(Emitter.emit(Top()), "Top.fir"))

    s = Simlite(Top(), harness_code=None, dpiconfig=cfg)
    s.step([20, 20])
    s.step([15, 100])
    s.step([1000, 2000])
    s.step([999, 2010])

```

## 仿真和混合仿真

## assert  

```python
from pyhcl import *


class AND(RawModule):
    io = IO(
        a=Input(U.w(1)),
        b=Input(U.w(1)),
        s=Output(U.w(1)),
    )

    myclock = Input(Clock())
    myreset = Input(Bool)
    io.s @= io.a ^ io.b
    _ = doAssert(myclock, io.a, io.s, "IF io.a is HIGH then io.s is HIGH")


if __name__ == '__main__':
    fa = AND()
    Emitter.dump(Emitter.emit(fa), "and.fir")
```

## 双向连接  
  
## 内联FIRRTL
## Features
As a novel hardware construction framework embedded in Python, PyHCL supports several useful features.
- Supports multiple data types: `UInt`, `SInt`, `Vector`, `Bundle`, `Clock`, `Memory`, and casual combination between them.
- Supports object-oriented inheritance, can compose modules by writing fewer codes.
- Supports functional programming
- Supports a bunch of convenient operations, such as the addition of `UInt`s, `SInt`s, `Vector`s and `Bundle`s.
- Supports the parameterization of variables, such as bit width, with the syntax facilities of the host language Python.


## TODO

- [ ] Supports more operations
- [ ] PyHCL's verification facility
