circuit PC :
  module PC :
    input clock : Clock
    input reset : UInt<1>
    output io : {flip pc_in : UInt<32>, pc_out : UInt<32>}
  
    reg pc : UInt<32>, clock with : 
      reset => (reset, UInt<32>("h0"))
    pc <= io.pc_in
    io.pc_out <= pc
