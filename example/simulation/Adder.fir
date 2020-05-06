circuit Adder :
  module FullAdder :
    input clock : Clock
    input reset : UInt<1>
    output io : {flip a : UInt<1>, flip b : UInt<1>, flip cin : UInt<1>, sum : UInt<1>, cout : UInt<1>}
  
    node a_xor_b = xor(io.a, io.b)
    node _T = xor(a_xor_b, io.cin)
    io.sum <= _T
    node a_and_b = and(io.a, io.b)
    node b_and_cin = and(io.b, io.cin)
    node _T_1 = or(a_and_b, b_and_cin)
    node a_and_cin = and(io.a, io.cin)
    node _T_2 = or(_T_1, a_and_cin)
    io.cout <= _T_2

  module Adder :
    input clock : Clock
    input reset : UInt<1>
    output io : {flip a : UInt<8>, flip b : UInt<8>, flip cin : UInt<1>, sum : UInt<8>, cout : UInt<1>}
  
    wire carry : UInt<1>[9]
    carry[0] <= io.cin
    inst _T of FullAdder
    _T.clock <= clock
    _T.reset <= reset
    node _T_1 = bits(io.a, 0, 0)
    _T.io.a <= _T_1
    node _T_2 = bits(io.b, 0, 0)
    _T.io.b <= _T_2
    _T.io.cin <= carry[0]
    carry[1] <= _T.io.cout
    wire sum : UInt<1>[8]
    sum[0] <= _T.io.sum
    inst _T_3 of FullAdder
    _T_3.clock <= clock
    _T_3.reset <= reset
    node _T_4 = bits(io.a, 1, 1)
    _T_3.io.a <= _T_4
    node _T_5 = bits(io.b, 1, 1)
    _T_3.io.b <= _T_5
    _T_3.io.cin <= carry[1]
    carry[2] <= _T_3.io.cout
    sum[1] <= _T_3.io.sum
    inst _T_6 of FullAdder
    _T_6.clock <= clock
    _T_6.reset <= reset
    node _T_7 = bits(io.a, 2, 2)
    _T_6.io.a <= _T_7
    node _T_8 = bits(io.b, 2, 2)
    _T_6.io.b <= _T_8
    _T_6.io.cin <= carry[2]
    carry[3] <= _T_6.io.cout
    sum[2] <= _T_6.io.sum
    inst _T_9 of FullAdder
    _T_9.clock <= clock
    _T_9.reset <= reset
    node _T_10 = bits(io.a, 3, 3)
    _T_9.io.a <= _T_10
    node _T_11 = bits(io.b, 3, 3)
    _T_9.io.b <= _T_11
    _T_9.io.cin <= carry[3]
    carry[4] <= _T_9.io.cout
    sum[3] <= _T_9.io.sum
    inst _T_12 of FullAdder
    _T_12.clock <= clock
    _T_12.reset <= reset
    node _T_13 = bits(io.a, 4, 4)
    _T_12.io.a <= _T_13
    node _T_14 = bits(io.b, 4, 4)
    _T_12.io.b <= _T_14
    _T_12.io.cin <= carry[4]
    carry[5] <= _T_12.io.cout
    sum[4] <= _T_12.io.sum
    inst _T_15 of FullAdder
    _T_15.clock <= clock
    _T_15.reset <= reset
    node _T_16 = bits(io.a, 5, 5)
    _T_15.io.a <= _T_16
    node _T_17 = bits(io.b, 5, 5)
    _T_15.io.b <= _T_17
    _T_15.io.cin <= carry[5]
    carry[6] <= _T_15.io.cout
    sum[5] <= _T_15.io.sum
    inst _T_18 of FullAdder
    _T_18.clock <= clock
    _T_18.reset <= reset
    node _T_19 = bits(io.a, 6, 6)
    _T_18.io.a <= _T_19
    node _T_20 = bits(io.b, 6, 6)
    _T_18.io.b <= _T_20
    _T_18.io.cin <= carry[6]
    carry[7] <= _T_18.io.cout
    sum[6] <= _T_18.io.sum
    inst _T_21 of FullAdder
    _T_21.clock <= clock
    _T_21.reset <= reset
    node _T_22 = bits(io.a, 7, 7)
    _T_21.io.a <= _T_22
    node _T_23 = bits(io.b, 7, 7)
    _T_21.io.b <= _T_23
    _T_21.io.cin <= carry[7]
    carry[8] <= _T_21.io.cout
    sum[7] <= _T_21.io.sum
    node _T_24 = cat(sum[7], sum[6])
    node _T_25 = cat(sum[5], sum[4])
    node _T_26 = cat(_T_24, _T_25)
    node _T_27 = cat(sum[3], sum[2])
    node _T_28 = cat(sum[1], sum[0])
    node _T_29 = cat(_T_27, _T_28)
    node _T_30 = cat(_T_26, _T_29)
    io.sum <= _T_30
    io.cout <= carry[8]
