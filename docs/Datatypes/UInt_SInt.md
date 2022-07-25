---
sort: 3
---
# UInt/SInt
## Description
The `U`/`S` type corresponds to a vector of bits that can be used for `signed`/`unsigned` integer arithmetic.
## Declaration

|                      Syntax                       |                             Description                              |    Return    |
|:-------------------------------------------------:|:--------------------------------------------------------------------:|:------------:|
|           U(value:Int)<br/>S(value:Int)           |     Create an unsigned/signed <br/>integer assigned with ‘value’     |   U<br/>S    |
|            U.w(x bits)<br/>S.w(x bits)            |          Create an unsigned/signed <br/>integer with x bits          |   U<br/>S    |
| U.w(x bits)(value:Int)<br/>S.w(x bits)(value:Int) | Create an unsigned/signed <br/>integer assigned with ‘value’, x bits |   U<br/>S    |

```python
U(1)	# 1-bit unsigend decimal value 1
U(0x126) # 12-bit unsigned hexadecimal value 0x126
U.w(4)(10) # 4-bit unsigned decimal value 10
S.w(16)(0x11) # 16-bit signed hexadecimal value 0x11
```
## Operators

The following operators are available for the U and S types:
### Logic

|  Operator  |              Description              |      Return       |
|:----------:|:-------------------------------------:|:-----------------:|
|   x ^ y    |              Bitwise XOR              | T(max(w(xy) bits) |
|     ~x     |              Bitwise NOT              |    T(w(x) bits    |
|   x & y    |              Bitwise AND              | T(max(w(xy) bits) |
| x &#124; y |              Bitwise OR               | T(max(w(xy) bits) |
|   x >> y   | 	Logical(U)/Arithmetic(S) shift right |   T(w(x) bits)    |
|   x << y   |          	Logical shift left          | T(w(x) + y bits)  |

```python
    Sa = S(32)
    Sc = Sa << 2

    Ua = U(31)
    Ub = U(2)
    Uc = ~(Ua & Ub)
    
    io.cout @= Uc ^ Ub | U(7)
    io.sout @= Sc
```

### Arithmetic

| Operator |        Description        |
|:--------:|:-------------------------:|
|  x + y   |    Arithmetic addition    |
|  x - y   |  Arithmetic subtraction   |
|  x * y   | Arithmetic multiplication |
|  x / y   |    Arithmetic division    |
|  x % y   |    Arithmetic modules     |
|   - x    |    Arithmetic negative    |

```python
# modules, subtraction
    temp = S(7) % S(3) - S(1)
```

### Comparison

| Operator |      Description      | Return |
|:--------:|:---------------------:|:------:|
|  x == y  |       Equality        |  Bool  |
|  x != y  |      Inequality       |  Bool  |
|  x > y   |     Greater than      |  Bool  |
|  x >= y  | Greater than or equal |  Bool  |
|  x < y   |      	Less than       |  Bool  |
|  x <= y  |  	Less than or equal  |  Bool  |

```python
# temp is U.w(1)
    temp = S(5) > S(3)
    io.sout @= temp
```
### Type cast!

|  Operator   | Description  |     Return      |
|:-----------:|:------------:|:---------------:|
| x.to_uint() | SInt to UInt | UInt(w(x) bits) |
| x.to_sint() | UInt to SInt | SInt(w(x) bits) |

```python
# cast uint to sint
    Ua = U(20)
    io.Sout @= Ua.to_sint()
```

### Bit extraction

### Misc

### FixPoint operations
#### Lower bit operations
#### High bit operations
#### fixTo function