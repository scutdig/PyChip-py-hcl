
# Combinatorial loop
## Introduction
PyHCL will check that there are no combinatorial loops in the design.
## example
The following code:
```python
class Top(Module):
    io = IO(
      count = Output(U.w(8))
    )
    a = Wire(U.w(8))
    b = Wire(U.w(8))

    b @= a
    io.count @= b
    a @= io.count
```
will throw :
```shell
pyhcl.ir.utils.TransformException: Loop do exist in graph: no independent nodes detected.
```
## False-positives
It should be said that PyHCL’s algorithm to detect combinatorial loops can be pessimistic, and it may give false positives. If it is giving a false positive, you can manually disable loop checking on one signal of the loop like so:
`# CheckCombLoop.run(self)`
```python
@dataclass(frozen=True)
class Block(Statement):
    stmts: List[Statement]

    def serialize(self) -> str:
        return '\n'.join([stmt.serialize() for stmt in self.stmts]) if self.stmts else ""

    def verilog_serialize(self) -> str:
        # CheckCombLoop.run(self)
        return '\n'.join([stmt.verilog_serialize() for stmt in self.stmts])

```