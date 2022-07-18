# Structuring

## module and hierarchy
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

## Clock domains

```python
class Counter(RawModule):
    io = IO(
        i=Input(Bool),
        o=Output(U.w(32)),
    )

    myclk = Clock()
    myrst = Reset()

    with clockdomin(myclk, myrst):
        r0 = RegInit(U.w(32)(0))

    with when(io.i):
        r0 @= r0 + U.w(32)(1)

    io.o @= r0
```

## Instamtiate Verilog IP

```python
class BBox(BlackBox):
    io = IO(
        in1=Input(U.w(64)),
        in2=Input(U.w(64)),
        out=Output(U.w(64)),
    )


class M(Module):
    io = IO(
        i = Input(U.w(64)),
        o = Output(U.w(64)),
    )

    bbox = BBox()
    bbox.io.in1 @= io.i
    bbox.io.in2 @= io.i
    io.o @= bbox.io.out

if __name__ == '__main__':
    Emitter.dumpVerilog(Emitter.dump(Emitter.emit(M()), "bbox.fir"))
```

## Parametrization

```python
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
```