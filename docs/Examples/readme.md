---
sort: 12
---

# Examples
## Introduction

Examples are split into three kinds:

- Simple examples that could be used to get used to the basics of PyHCL.

- Intermediate examples which implement components by using a traditional approach.

- Advanced examples which go further than traditional HDL by using object-oriented programming, functional programming, and meta-hardware description.

They are all accessible in the sidebar under the corresponding sections.

## Getting started
All examples assume that you have the following imports on the top of your scala file:

```python
from pyhcl import *
```

To generate `Verilog`, `highFirrtl`, `lowFirrtl` for a given Module, you can place the following at the bottom of your python file:

```python
if __name__ == '__main__':
    # emit high firrtl
    Emitter.dump(Emitter.emit(FullAdder(), HighForm), "FullAdder.fir")
    # emit lowered firrtl
    Emitter.dump(Emitter.emit(FullAdder(), LowForm), "FullAdder.lo.fir")
    # emit verilog
    Emitter.dump(Emitter.emit(FullAdder(), Verilog), "FullAdder.v")
```


{% include list.liquid %}