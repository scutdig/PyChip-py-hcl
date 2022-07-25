---
sort: 1
---

# Module and hierarchy
## Introduction

* All circle must extends `Module`

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

## Input / output definition
The syntax to define inputs and outputs is as follows:

|        Syntax         |               Description               |
|:---------------------:|:---------------------------------------:|
|  Input/Output(Bool)   |       Create an Bool input/output       |
| Input/Output(U.w(x))  | Create an UInt input/output with x bits |
| Input/Output(S.w(x))  | Create an SInt input/output with x bits |

Components can only read output and input signals of child components.

* Components can only read output and input signals of child components.
* Components can read their own output port values.


## Pruned signals
PyHCL will generate all the named signals and their depedencies, while all the useless anonymous / zero width ones are removed from the RTL generation

## Parametrized Hardware

If you want to parameterize your component, you can give parameters to the constructor of the component as follows:

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

## Synthesized Module names

Within a module, each component has a name, called a `partial name`. The `full` name is built by joining every component’s parent name with `_`, for example: `io_clockDomain_reset`.