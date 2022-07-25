---
sort: 6
---
# Vec
## Description
Vector is most commonly used to defined an array of wire. 

## Declaration
To defined a vector, we use Vec to do so:

```python
Vec(<size>, <cdatatype>)
```

size indicate the size of the vector, cdatatype indicate the datatype of the vector, and it must be a basic datatype(U, S, Bool). For example, we define an array of wire:

```python
rarray = Wire(Vec(4, U.w(16)))	# A 16-bit 4 length unsigned integer wire array
```

#### example

We could also index the wire array with the operator [], as the built-in operator of Python:

```python
# rarray = [U(0), U(1), U(2), U(3)]
for i in range(0, 4):
  rarray[i] <<= U(i)
```

Another commonly used of Vec is using in I/O ports. We define a input port a using Vec:
```python
a=Input(Vec(4, U.w(16)))
```
Which is convenience for multiple inputs or outputs.

> Vec in PyHCL would translate as the array definition in FIRRTL, and compile to Verilog. However, the array features may lost in Verilog code. For example, the vector of input port a above, after compile to Verilog:
> ```python
> input  [15:0] io_a_0,
> input  [15:0] io_a_1,
> input  [15:0] io_a_2,
> input  [15:0] io_a_3,
>```
> We could see that it has divide into 4 individual ports.

## Operations
The following operators are available for the `Vec` type:
### Comparison
### Type cast
### Misc

|  Operator  |         Description          | Return |
|:----------:|:----------------------------:|:------:|
| x.length() | return the length of the Vec |  Int   |
|  x.size()  | return the length of the Vec |  Int   |

```python
    sum1 = Wire(Vec(20, U.w(16)))
    print(sum1.size()) # 20
```
### Lib helper functions