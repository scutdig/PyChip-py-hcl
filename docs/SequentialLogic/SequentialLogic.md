# Sequential Logic

## Registers
* Retain state until updated:
  
```python
reg = Reg(U.w(32))
counter = RegInit(U.w(32)(0))
```

## RAM/ROM/Mem

```python
class MemDemo(Module):
    io = IO(
        i=Input(U.w(8)),
        o=Output(U.w(8)),
    )

    m = Mem(10, U.w(8))
    m[U(2)] @= io.i
    io.o @= m[U(2)]
```