# PyHCL
[![Build Status](https://travis-ci.com/scutdig/py-hcl.svg?branch=master)](https://travis-ci.com/scutdig/py-hcl)
[![codecov](https://codecov.io/gh/scutdig/py-hcl/branch/master/graph/badge.svg)](https://codecov.io/gh/scutdig/py-hcl)
[![PyPI](https://img.shields.io/pypi/v/py-hcl.svg)](https://pypi.python.org/pypi)

PyHCL is a hardware construct language like [Chisel](https://github.com/freechipsproject/chisel3) but more lightweight and more relaxed to use.
As a novel hardware construction framework embedded in Python, PyHCL supports several useful features include object-oriented, functional programming,
and dynamically typed objects.

The goal of PyHCL is providing a complete design and verification tool flow for heterogeneous computing systems flexibly using the same design methodology.

PyHCL is powered by [FIRRTL](https://github.com/freechipsproject/firrtl), an intermediate representation for digital circuit design.

PyHCL-generated circuits can be compiled to the widely-used HDL Verilog.

Attention: The back end of the compilation is highly experimental.


## Simple Example

### Writing A Full Adder
PyHCL defines modules using only simple Python syntax that looks like this:
```python
from pyhcl import *

class FullAdder(Module):
    io = IO(
        a=Input(Bool),
        b=Input(Bool),
        cin=Input(Bool),
        sum=Output(Bool),
        cout=Output(Bool),
    )

    # Generate the sum
    io.sum @= io.a ^ io.b ^ io.cin

    # Generate the carry
    io.cout @= io.a & io.b | io.b & io.cin | io.a & io.cin
```

### Compiling To High FIRRTL

Compiling module by calling `compile_to_highform`:
```python
Emitter.dump(Emitter.emit(FullAdder(), HighForm), "FullAdder.fir")
```

Will generate the following FIRRTL codes:
```
circuit FullAdder :
  module FullAdder :
    input clock : Clock
    input reset : UInt<1>
    output io : {flip a : UInt<1>, flip b : UInt<1>, flip cin : UInt<1>, s : UInt<1>, cout : UInt<1>}
  
    node _T = xor(io.a, io.b)
    node _T_1 = xor(_T, io.cin)
    io.s <= _T_1
    node _T_2 = and(io.a, io.b)
    node _T_3 = and(io.a, io.cin)
    node _T_4 = or(_T_2, _T_3)
    node _T_5 = and(io.b, io.cin)
    node _T_6 = or(_T_4, _T_5)
    io.cout <= _T_6
```

### Compiling To Lowered FIRRTL

Compiling module by calling `compile_to_lowform`:

```python
Emitter.dump(Emitter.emit(FullAdder(), LowForm), "FullAdder.lo.fir")
```

Will generate the following FIRRTL codes:

```
circuit FullAdder :
  module FullAdder :
    input clock : Clock
    input reset : UInt<1>
    input io_a : UInt<1>
    input io_b : UInt<1>
    input io_cin : UInt<1>
    output io_s : UInt<1>
    output io_cout : UInt<1>
  
    node _T = xor(io_a, io_b)
    node _T_1 = xor(_T, io_cin)
    io_s <= _T_1
    node _T_2 = and(io_a, io_b)
    node _T_3 = and(io_a, io_cin)
    node _T_4 = or(_T_2, _T_3)
    node _T_5 = and(io_b, io_cin)
    node _T_6 = or(_T_4, _T_5)
    io_cout <= _T_6
```

### Compiling To Verilog

Compiling module by calling `compile_to_verilog`:

```shell
Emitter.dump(Emitter.emit(FullAdder(), Verilog), "FullAdder.v")
```

Then `FullAdder.v` will be generated:
```verilog
module FullAdder(
  input		clock,
  input		reset,
  input		io_a,
  input		io_b,
  input		io_cin,
  output		io_s,
  output		io_cout
);

  assign io_s = io_a ^ io_b ^ io_cin;
  assign io_cout = io_a & io_b | io_a & io_cin | io_b & io_cin;
  
endmodule
```


## Features

- Supports multiple data types: `UInt`, `SInt`, `Vector`, `Bundle`, `Clock`, `Memory`, and casual combination between them.
- Supports object-oriented inheritance, can compose modules by writing fewer codes.
- Supports a bunch of convenient operations, such as the addition of `UInt`s, `SInt`s, `Vector`s and `Bundle`s.
- Supports the parameterization of variables, such as bit width, with the syntax facilities of the host language Python.


## TODO

- [ ] Supports more operations
- [ ] PyHCL's verification facility
