---
sort: 5
---
# Bundle！
## Description
The Bundle is a composite type that defines a group of named signals (of any PyHCL basic type) under a single name. It is similar to Chisel Bundle. Actually, in PyHCL's core library, IO is actually a Bundle and translate to FIRRTL later on. As a beginner of PyHCL, you could simply treat Bundle as the struct data structure of C/C++.
## Declaration
The way we define a Bundle is similar to IO:
```python
bun = Bundle(
  x=U.w(16),
  y=S.w(16),
  z=Bool
)
```
`x`, `y`, and `z` are the subfield of Bundle. `Bundle` is a datatype, so it must used in a circuit element:
```python
breg = Reg(Bundle(
  x=U.w(16),
  y=S.w(16),
  z=Bool
))
```
We use `.` operator to access the subfield of the `Bundle`, similar to IO:
```python
breg.x <<= U(12)
breg.y <<= S(4)
breg.z <<= Bool(False)
io.out <<= breg.x
```
> Bundle is still an experimental feature of PyHCL, we suggest that you only include basic types in Bundle.

### Conditional signals

## Operators
### Comparison
### Type cast
### Convert Bits back to Bundle
## IO Element direction