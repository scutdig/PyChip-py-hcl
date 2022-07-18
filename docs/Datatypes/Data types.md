# Data Types

- Supports multiple data types: `UInt`, `SInt`, `Vector`, `Bundle`, `Clock`, `Memory`, and casual combination between them.
- Supports object-oriented inheritance, can compose modules by writing fewer codes.
- Supports a bunch of convenient operations, such as the addition of `UInt`s, `SInt`s, `Vector`s and `Bundle`s.
- Supports the parameterization of variables, such as bit width, with the syntax facilities of the host language Python.


## UInt/SInt
* `U(N.w)`: length `N` unsigned integer that includes Bits operators and
  unsigned arithmetic (e.g. `+`, `-`, ...) and comparison operators (e.g.
  `<`, `<=`, ...)
* `S(N.w)`: length `N` signed integer that includes Bits operators and
  signed arithmetic (e.g. `+`, `-`, ...) and comparison operators (e.g.
  `<`, `<=`, ...)

## Bool
* `Bool`: bool value，which is `U(1.w)`
* `true, false`: boolean literals

## Clock
* `Clock`: bool value，which is `U(1.w)`
* `true, false`: boolean literals


## Bundle
* `Input(T)`, `Output(T)` qualify type `T` to be an input, output, and
respectively.
* `IO(T)` qualify type `T` to be an input, output, and
respectively.

## Vec
* `Vec(4, U.w(32))`: fixed length array of length `4` containing values of type
  `U.w(32)` with equality operator (`==`) defined

## Registers

* Retain state until updated:
```python
reg = Reg(U.w(32))
counter = RegInit(U.w(32)(0))
```

## Memories

```python
m = Mem(10, U.w(8))
m[U(2)] @= io.i
io.o @= m[U(2)]
```

## Circuits
**Defining**:  `Module`

```python
from pyhcl import *
from pyhcl.simulator import Simulator

class FullAdder(Module):
    io = IO(
        a=Input(Bool),
        b=Input(Bool),
        cin=Input(Bool),
        sum=Output(Bool),
        cout=Output(Bool),
    )

    # Generate the sum
    a_xor_b = io.a ^ io.b
    io.sum @= a_xor_b ^ io.cin

    # Generate the carry
    a_and_b = io.a & io.b
    b_and_cin = io.b & io.cin
    a_and_cin = io.a & io.cin
    io.cout @= a_and_b | b_and_cin | a_and_cin
```
**Usage**: circuits are used by instancing them inside another definitions and
  their ports are accessed using dot notation

```python
FA = FullAdder()
```

**Metaprogramming**: abstract over parameters by generating a circuit definition inside a closure

```python
def adder(n: int):
    class Adder(Module):
        io = IO(
            a=Input(U.w(n)),
            b=Input(U.w(n)),
            cin=Input(Bool),
            sum=Output(U.w(n)),
            cout=Output(Bool),
        )

        FAs = [FullAdder().io for _ in range(n)]
        carry = Wire(Vec(n + 1, Bool))
        sum = Wire(Vec(n, Bool))

        carry[0] @= io.cin

        for i in range(n):
            FAs[i].a @= io.a[i]
            FAs[i].b @= io.b[i]
            FAs[i].cin @= carry[i]
            carry[i + 1] @= FAs[i].cout
            sum[i] @= FAs[i].sum

        io.sum @= CatVecH2L(sum)
        io.cout @= carry[n]

    return Adder()
```

# Operators
## Infix operators
All types support the following operators:
- Equal `==`
- Not Equal `!=`

The `Bool` type supports the following logical operators.
- And `&`
- Or `|`
- Exclusive or `^`
- Not `~`


The `UInt` and `SInt` types support all the logical operators
as well as arithmetic and comparison operators.
- Add `+`
- Subtract/Negate `-`
- Multiply `*`
- Divide `/`
- Less than `<`
- Less than or equal `<=`
- Greater than `>`
- Greater than or equal `>=`

Note that the the right shift operator when applied to an `SInt` becomes
an arithmetic shift right operator (which replicates the sign bit as it shifts right).

## Combinational

```python
# Mux(<选择信号>, <真输出>, <假输出>)
io.z @= Mux(io.sel, io.b, io.a)
```

## Sequential

```python
class Register(Module):
    io = IO(
        out=Output(U.w(32))
    )

    counter = RegInit(U.w(32)(0))
    counter @= counter + U(1)
    io.out @= counter
```