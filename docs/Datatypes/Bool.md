---
sort: 1
---
# Bool

## Description
The Bool type corresponds to `U.w(1)`.
## Declaration
The syntax to declare a boolean value is as follows:

|        Syntax        |                             Description                              |     Return    |
|:--------------------:|:--------------------------------------------------------------------:|:-------------:|
|         Bool         |                            Create a Bool                             |     U.w(1)    |
| Bool(value: Boolean) | Create a Bool <br/>assigned with a Python Boolean<br/> (true, false) | U.w(1)(value) |

```python
myBool_1 = Bool         # Create a Bool
myBool_1 = Bool(True)
myBOol_2 = Bool(3>5)    # same as Bool(False)
io.cout @= myBool_1     # @= is the assignment operator
```
## Operators
All operators available for the Bool type is same as `U.w(1)`