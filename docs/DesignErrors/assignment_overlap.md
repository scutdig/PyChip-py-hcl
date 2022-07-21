
# Assignment overlap


## Introduction


Pyhcl will check that no signal assignment completely erases a previous one.

## Example

The following code

```scala

   class TopLevel extends Component {
     val a = UInt(8 bits)
     a := 42
     a := 66 // Erase the a := 42 assignment
   }
```

will throw the following error:


```   
ASSIGNMENT OVERLAP completely the previous one of (toplevel/a :  UInt[8 bits])
     ***
     Source file location of the a := 66 assignment via the stack trace
     ***
```

A fix could be:


```python
   class TopLevel extends Component {
     val a = UInt(8 bits)
     a := 42
     when(something) {
       a := 66
     }
   }
```

But in the case when you really want to override the previous assignment (as there are times when overriding makes sense), you can do the following:


```scala
   class TopLevel extends Component {
     val a = UInt(8 bits)
     a := 42
     a.allowOverride
     a := 66
   }
```


# Clock Crossing violation
## Introduction
## example
### crossClockDomain tag
### setSyncronouswith
### BufferCC


# Combinatorial loop
## Introduction
## example
## False-positives


# Hierarchy violation
## Introduction
## example


# IO Bundel
## Introduction
## example


# Latch detected
## Introduction
## example


# No driver on
## Introduction
## example

# NullPointerException
## Introduction
## example
### Issue explanation


# Register defined as component input
## Introduction
## example


# Scope violation
## Introduction
## example


# PyHCL can't clone class
## Introduction
## Example1
## Example2


# Unassigned register
## Introduction
## Example
## Register with only init

# Unreachable is statement
## Introduction
## Example


# Width mismatch
## Assignment example
## Operator example

# Introduction