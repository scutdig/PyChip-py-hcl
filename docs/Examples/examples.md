# Simple ones
## APB3 definition
### Introduction
This example will show the syntax to define an APB3 `Bundle`.
### Specification
The specification from ARM could be interpreted as follows:

| Signal Name   | Type                  |  Driver side      |  Comment |
| :--------     | :----------------     | :--------         | :----------------|
|PADDR|U.w(addressWidth)|Master|Address in byte|
|PSEL|U.w(selWidth)|Master|One bit per slave|
|PENABLE|Bool|Master||
|PWRITE|Bool|Master||
|PWDATA|U.w(dataWidth)|Master||
|PREADY|Bool|Slave||
|PRDATA|U.w(dataWidth)|Slave||
|PSLVERROR|Bool|Slave|Optional|

### Implementation

### Usage


## Carry adder
This example defines a component with inputs `a`, `b` and `cin`, and `sum`, `cout` output. At any time, result will be the `a`, `b` and `cin` (combinatorial). The `sum`, `cout` are manually done by a carry adder logic.
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
## Color summing
## Counter with clear
```python
from pyhcl import *

def counter(width: int):
    class Counter(Module):
        io = IO(
            clear=Input(Bool),
            result=Output(U.w(width))
        )
        register = RegInit(U.w(width)(0))
        register @= register + U(1)
        with when(io.clear):
            register @= U(0)
        io.result @= register
    return Counter()
```
## PLL BlackBox and reset controller
### The PLL BlackBox definition
### TopLevel definition
## RGB to gray
## Sinus rom

# Intermediates ones
## Fractal calculator
### Introduction
### Specification
### Elaboration parameters(Generics)
### Bundle definition
### Component implementation
## UART
### Specification
### Data structures
### Implementation
### Simple usage
### Example with test bench
### Bonus: Having fun with Stream
## VGA
### Introduction
### Data structures
### VGA Controller




# Advanced ones
## JTAG TAP
### Introduction
### JTAG bus
### JTAG state machine
### JTAG TAP
### Jtag instructions
### User friendly wrapper
### Usage demonstration
## Memory mapped UART
### Instroduction
### Specification
### Implementation
## Pinesec
## Timer 
### Introduction
### Timer
### Bridging function






# Examples

## Simple ones
* Full_Adder
  
```python
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

## Advanced ones
* Filter
  
```python
from functools import reduce
from typing import List

from pyhcl import *

def myManyDynamicElementVecFir(length: int, consts: List):
    class MyManyDynamicElementVecFir(Module):
        io = IO(
            i=Input(U.w(8)),
            valid=Input(Bool),
            o=Output(U.w(8)),
        )

        taps = [io.i] + [RegInit(U.w(8)(0)) for _ in range(length)]
        for a, b in zip(taps, taps[1:]):
            with when(io.valid):
                b @= a

        m = map(lambda x: x[0] * x[1], zip(taps, consts))
        io.o @= reduce(lambda x, y: x + y, m)

    return MyManyDynamicElementVecFir()


def main():
    consts = []
    for i in range(4):
        consts.append(U(i))
    f = Emitter.dump(Emitter.emit(myManyDynamicElementVecFir(4, consts)), "filter.fir")
    Emitter.dumpVerilog(f)


if __name__ == '__main__':
    main()
```

* Neurons
  
```python
from pyhcl import *

W = 8  # 位宽

def matrixMul(x: int, y: int, z: int):
    """
    x*y × y*z 矩阵乘法电路
    """

    class MatrixMul(Module):
        io = IO(
            a=Input(Vec(x, Vec(y, U.w(W)))),
            b=Input(Vec(y, Vec(z, U.w(W)))),
            o=Output(Vec(x, Vec(z, U.w(W)))),
        )

        for i, a_row in enumerate(io.a):
            for j, b_col in enumerate(zip(*io.b)):
                io.o[i][j] @= Sum(a * b for a, b in zip(a_row, b_col))

    return MatrixMul()


def bias(n):
    return U.w(W)(n)


def weight(lst):
    return VecInit(U.w(W)(i) for i in lst)


def neurons(w, b):
    """
    参数：权重向量 w，偏移量 b
    输出：神经网络神经元电路  *注：暂无通过非线性传递函数
    """

    class Unit(Module):
        io = IO(
            i=Input(Vec(len(w), U.w(W))),
            o=Output(U.w(W))
        )
        m = matrixMul(1, len(w), 1).io
        m.a @= io.i

        m.b @= w
        io.o @= m.o[0][0] + b

    return Unit()

def main():
    # 得到权重向量为[3, 4, 5, 6, 7, 8, 9, 10]，偏移量为14的神经元电路
    n = neurons(weight([3, 4, 5, 6, 7, 8, 9, 10]), bias(14))
    f = Emitter.dump(Emitter.emit(n), "neurons.fir")
    Emitter.dumpVerilog(f)

if __name__ == '__main__':
    main()
```
