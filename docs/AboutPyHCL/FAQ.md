---
sort: 1
---
# FAQ
## What is the overhead of PyHCL generated RTL compared to human written Verilog?
PyHCL is a hardware construct language like [Chisel](https://github.com/freechipsproject/chisel3) but more lightweight and more relaxed to use.

## What if PyHCL becomes unsupported in the future?
This question has two sides:

1. PyHCL generates Verilog files, which means that PyHCL will be supported by all EDA tools for many decades.

2. If there is a bug in PyHCL and there is no longer support to fix it, it’s not a deadly situation, because the PyHCL compiler is fully open source. For simple issues, you may be able to fix the issue yourself in few hours. Remember how much time it takes to EDA companies to fix issues or to add new features in their closed tools.

## Does PyHCL keep comments in generated verilog?
No, it doesn’t. Generated files should be considered as a netlist.
## Could PyHCL scale up to big projects?
PyHCL is powered by [FIRRTL](https://github.com/freechipsproject/firrtl), an intermediate representation for digital circuit design.

PyHCL-generated circuits can be compiled to the widely-used HDL Verilog.

Attention: The back end of the compilation is highly experimental.
## How PyHCL came to be?
The dominant hardware design languages in industry are **Verilog** and **VHDL**, however this procedural language, which has been around for decades, can no longer meet the needs of today's increasingly large and complex integrated circuit chip development.

**Chisel**, the pioneer of combining hardware design with high-level programming languages, has proposed the possibility of agile design for hardware by embedding hardware design into the high-level programming language Scala. Embedding a hardware design framework into an object-oriented programming language allows hardware design to enjoy the advantages of object-oriented language ontologies.

However, since Chisel is based on Scala, this language has a small audience, is difficult to learn, and has a low community activity, making it difficult to get started and the learning time period is long, which is not conducive to its promotion. Therefore, our team uses the Python language to design and develop PyHCL to provide a more easy-to-use and concise hardware design framework.

## Why develop a new language when there is VHDL/Verilog/SystemVerilog?
The goal of PyHCL is providing a complete design and verification tool flow for heterogeneous computing systems flexibly using the same design methodology.
## How to use an unreleased version of PyHCL (but committed on git)?

