circuit FullAdder :
  module FullAdder :
    input clock : Clock
    input reset : UInt<1>
    output io : {flip a : UInt<1>, flip b : UInt<1>, flip cin : UInt<1>, s : UInt<1>, cout : UInt<1>}
  
    node _T = xor(io.a, io.b)
    node _T_1 = xor(_T, io.cin)
    io.s <= _T_1
    node _T_2 = and(io.a, io.b)
    node _T_3 = and(io.a, io.cin)
    node _T_4 = or(_T_2, _T_3)
    node _T_5 = and(io.b, io.cin)
    node _T_6 = or(_T_4, _T_5)
    io.cout <= _T_6
