# Welcome to the PyHCL Documentation

## Site purpose and structure

This site presents the PyHCL language and how to use it on concrete examples.

## What is PyHCL

PyHCL is a hardware construct language like [Chisel](https://github.com/freechipsproject/chisel3) but more lightweight and more relaxed to use.
As a novel hardware construction framework embedded in Python, PyHCL supports several useful features include object-oriented, functional programming,
and dynamically typed objects.

The goal of PyHCL is providing a complete design and verification tool flow for heterogeneous computing systems flexibly using the same design methodology.

PyHCL is powered by [FIRRTL](https://github.com/freechipsproject/firrtl), an intermediate representation for digital circuit design. With the FIRRTL 
compiler framework, PyHCL-generated circuits can be compiled to the widely-used HDL Verilog.  


## Similar Projects

* [autofpga](https://github.com/ZipCPU/autofpga) - C++, A utility for Composing FPGA designs from Peripherals
* [BinPy](https://github.com/BinPy/BinPy) - Python, An electronic simulation library
* [blarney](https://github.com/blarney-lang/blarney) - Haskell, HCL
* [bsc](https://github.com/B-Lang-org/bsc) - Haskell, C++, BSV - Bluespec Compiler
* [chisel](https://chisel.eecs.berkeley.edu/) - 2012-?, Scala, HCL
* [Chips-2.0](https://github.com/dawsonjon/Chips-2.0) - , , FPGA Design Suite based on C to Verilog design flow
* [circt](https://github.com/llvm/circt) - 2020-?, C++/LLVM, compiler infrastructure
* [circuitgraph](https://github.com/circuitgraph/circuitgraph) - Tools for working with circuits as graphs in python
* [concat](https://github.com/conal/concat) - 2016-?, Haskell, Haskell to hardware
* [DUH](https://github.com/sifive/duh) - JS, simple convertor between verilog/scala/ipxact
* [DFiant](https://github.com/DFiantHDL/DFiant) 2019-?, Scala, dataflow based HDL
* [edalize](https://github.com/olofk/edalize) - 2018-?, Python, abstraction layer for eda tools
* [garnet](https://github.com/StanfordAHA/garnet) -2018-?, Python, Coarse-Grained Reconfigurable Architecture generator based on magma
* [hammer](https://github.com/ucb-bar/hammer) - 2017-?, Python, Highly Agile Masks Made Effortlessly from RTL
* [heterocl](https://github.com/cornell-zhang/heterocl) - 2017-?, C++, A Multi-Paradigm Programming Infrastructure for Software-Defined Reconfigurable Computing
* [hoodlum](https://github.com/tcr/hoodlum) - 2016-?, Rust, HCL
* [ILAng](https://github.com/Bo-Yuan-Huang/ILAng) - modeling and verification platform for SoCs where Instruction-Level Abstraction (ILA) is used as the formal model for hardware components.
* :skull: [jhdl](https://github.com/larsjoost/jhdl) - ?-2017, C++ Verilog/VHDL -> systemC, prototype
* [Kactus2](http://funbase.cs.tut.fi) - IP-core packager
* [kratos](https://github.com/Kuree/kratos) - C++/Python, hardware generator/simulator
* [lgraph](https://github.com/masc-ucsc/lgraph) - C, generic graph library
* [llhd](https://github.com/fabianschuiki/llhd) - Rust, HCL
* [livehd](https://github.com/masc-ucsc/livehd) - mainly C++, An infrastructure designed for Live Hardware Development.
* [Lucid HDL in Alchitry-Labs](https://github.com/alchitry/Alchitry-Labs) - Custom language and IDE inspired by Verilog
* [magma](https://github.com/phanrahan/magma/) - 2017-?, Python, HCL
* [migen](https://github.com/m-labs/migen) - 2013-?, Python, HCL
* [mockturtle](https://github.com/lsils/mockturtle) - logic network library
* [moore](https://github.com/fabianschuiki/moore) - Rust, HDL -> model compiler
* [MyHDL](https://github.com/myhdl/myhdl) - 2004-?, Python, Process based HDL
* [nmigen](https://github.com/m-labs/nmigen) -, Python, A refreshed Python toolbox for building complex digital hardware
* [OpenTimer](https://github.com/OpenTimer/OpenTimer) - , C++,  A High-Performance Timing Analysis Tool for VLSI Systems
* [percy](https://github.com/whaaswijk/percy) - Collection of different synthesizers and exact synthesis methods for use in applications such as circuit resynthesis and design exploration.
* [PyChip-py-hcl](https://github.com/scutdig/PyChip-py-hcl) - , Python, Chisel3 like HCL
* [pygears](https://github.com/bogdanvuk/pygears) - , Python, function style HDL generator
* [PyMTL3](https://github.com/cornell-brg/pymtl3) 2018-?
* [PyMTL](https://github.com/cornell-brg/pymtl) - 2014-?, Python, Process based HDL
* [PipelineC](https://github.com/JulianKemmerer/PipelineC) - 2018-?, Python, C++ HLS-like automatic pipelining as a language construct/compiler
* [PyRTL](https://github.com/UCSBarchlab/PyRTL) - 2015-?, Python, HCL
* [Pyverilog](https://github.com/PyHDI/Pyverilog) - 2013-? Python-based Hardware Design Processing Toolkit for Verilog HDL
* [rogue](https://github.com/slaclab/rogue) , C++/Python - Hardware Abstraction & Data Acquisition System
* [sail](https://github.com/rems-project/sail) 2018-?, (OCaml, Standard ML, Isabelle) - architecture definition language
* [spatial](https://github.com/stanford-ppl/spatial) - Scala, an Argon DSL like, high level abstraction
* [SpinalHDL](https://github.com/SpinalHDL/SpinalHDL) - 2015-?, Scala, HCL
* [Silice](https://github.com/sylefeb/Silice) - ?, C++, Custom HDL
* :skull: [SyDpy](https://github.com/bogdanvuk/sydpy) - ?-2016, Python, HCL and verif. framework operating on TML/RTL level
* [systemrdl-compiler](https://github.com/SystemRDL/systemrdl-compiler) - Python,c++, register description language compiler
* [UHDM](https://github.com/alainmarcel/UHDM) - C++ SystemVerilog -> C++ model
* :skull: [Verilog.jl](https://github.com/interplanetary-robot/Verilog.jl) - 2017-2017, Julia, simple Julia to Verilog transpiler
* [veriloggen](https://github.com/PyHDI/veriloggen) - 2015-?, Python, Verilog centric HCL with HLS like features
* :skull:  [wyre](https://github.com/nickmqb/wyre) - 2020-2020, Mupad, Minimalistic HDL
* [phi](https://github.com/donn/Phi) - 2019-?, custom language, llvm based compiler of custom hdl
* [prga](https://github.com/PrincetonUniversity/prga) - 2019-?. Python, prototyping platform with integrated yosys





See the sidebar for various pages.
<!-- 关于模板说明，docs为整个文档的根目录，其下文件夹为一级目录, 每一级目录的readme.md为该级目录的索引 -->

<!--  pkill -f jekyll 杀
      bundle exec jekyll serve 开
-->

* [About PyHCL](./AboutPyHCL/readme.md)
* [Data types](./Datatypes/readme.md)
* [Examples](./Examples/readme.md)
* [Getting Stated](./GettingStarted/readme.md)

<!-- 
仿照spinalhdl来写
.关于：说明
.开始：安装
.数据类型：Bool，bits，这些
.语法：赋值，选择，
.等级：module，，，
.时序逻辑：多时钟域
.仿真
.例子：滤波器设计。。。
.提升：
 -->

