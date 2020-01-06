# PyHCL
[![Build Status](https://travis-ci.com/scutdig/py-hcl.svg?branch=master)](https://travis-ci.com/scutdig/py-hcl)
[![codecov](https://codecov.io/gh/scutdig/py-hcl/branch/master/graph/badge.svg)](https://codecov.io/gh/scutdig/py-hcl)
[![PyPI](https://img.shields.io/pypi/v/py-hcl.svg)](https://pypi.python.org/pypi)

PyHCL is a hardware construct language like [Chisel](https://github.com/freechipsproject/chisel3) but more lightweight and more relaxed to use.
As a novel hardware construction framework embedded in Python, PyHCL supports several useful features include object-oriented, functional programming,
and dynamically typed objects.

The goal of PyHCL is providing a complete design and verification tool flow for heterogeneous computing systems flexibly using the same design methodology.

PyHCL is powered by [FIRRTL](https://github.com/freechipsproject/firrtl), an intermediate representation for digital circuit design. With the FIRRTL 
compiler framework, PyHCL-generated circuits can be compiled to the widely-used HDL Verilog.  


## Getting Started

#### Installing PyHCL

```shell script
$ pip install py-hcl
```

#### Writing A Full Adder
PyHCL defines modules using only simple Python syntax that looks like this:
```python
from py_hcl import *

class FullAdder(Module):
    io = IO(
        a=Input(Bool),
        b=Input(Bool),
        cin=Input(Bool),
        sum=Output(Bool),
        cout=Output(Bool),
    )

    # Generate the sum
    io.sum <<= io.a ^ io.b ^ io.cin

    # Generate the carry
    io.cout <<= io.a & io.b | io.b & io.cin | io.a & io.cin
```

#### Compiling To FIRRTL

Compiling module by calling `compile_to_firrtl`:
```python
compile_to_firrtl(FullAdder, 'full_adder.fir')
```

Will generate the following FIRRTL codes:
```
circuit FullAdder :
  module FullAdder :
    input clock : Clock
    input reset : UInt<1>
    input FullAdder_io_a : UInt<1>
    input FullAdder_io_b : UInt<1>
    input FullAdder_io_cin : UInt<1>
    output FullAdder_io_sum : UInt<1>
    output FullAdder_io_cout : UInt<1>

    node _T_0 = xor(FullAdder_io_a, FullAdder_io_b)
    node _T_1 = xor(_T_0, FullAdder_io_cin)
    FullAdder_io_sum <= _T_1
    node _T_2 = and(FullAdder_io_a, FullAdder_io_b)
    node _T_3 = and(FullAdder_io_b, FullAdder_io_cin)
    node _T_4 = or(_T_2, _T_3)
    node _T_5 = and(FullAdder_io_a, FullAdder_io_cin)
    node _T_6 = or(_T_4, _T_5)
    FullAdder_io_cout <= _T_6
```

#### Compiling To Verilog

While FIRRTL is generated, PyHCL's job is complete. To further compile to Verilog, the [FIRRTL compiler framework](
https://github.com/freechipsproject/firrtl) is required:

```shell script
$ firrtl -i full_adder.fir
```

Then `FullAdder.v` will be generated:
```verilog
module FullAdder(
  input   clock,
  input   reset,
  input   FullAdder_io_a,
  input   FullAdder_io_b,
  input   FullAdder_io_cin,
  output  FullAdder_io_sum,
  output  FullAdder_io_cout
);
  wire  _T_0;
  wire  _T_2;
  wire  _T_3;
  wire  _T_4;
  wire  _T_5;
  assign _T_0 = FullAdder_io_a ^ FullAdder_io_b;
  assign _T_2 = FullAdder_io_a & FullAdder_io_b;
  assign _T_3 = FullAdder_io_b & FullAdder_io_cin;
  assign _T_4 = _T_2 | _T_3;
  assign _T_5 = FullAdder_io_a & FullAdder_io_cin;
  assign FullAdder_io_sum = _T_0 ^ FullAdder_io_cin;
  assign FullAdder_io_cout = _T_4 | _T_5;
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