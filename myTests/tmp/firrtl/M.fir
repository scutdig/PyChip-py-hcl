circuit M :
  module Add :
      input in1 : UInt<32>
      input in2 : UInt<32>
      output out : UInt<32>
      out <= add(in1, in2)

  module M :
    input clock : Clock
    input reset : UInt<1>
    output io : {flip a : UInt<32>, flip b : UInt<32>, c : UInt<32>}
  
    inst bbox of Add
    
    bbox.in1 <= io.a
    
    bbox.in2 <= io.b
    
    io.c <= bbox.out
