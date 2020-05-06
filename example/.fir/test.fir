circuit Test :
  module Test :
    input clock : Clock
    input reset : UInt<1>
    output io : {DIO_stop : UInt<1>, Jotaro_stop : UInt<1>}
  
    reg counter : UInt<32>, clock with : 
      reset => (reset, UInt<32>("h0"))
    node _T = add(counter, UInt<1>("h1"))
    counter <= _T
    node _T_1 = eq(counter, UInt<4>("ha"))
    reg DIO_stop_r : UInt<1>, clock with : 
      reset => (reset, UInt<1>("h1"))
    when _T_1 :
      io.DIO_stop <= UInt<1>("h0")
      DIO_stop_r <= UInt<1>("h0")
    else :
      io.DIO_stop <= DIO_stop_r
    node _T_2 = eq(io.DIO_stop, UInt<1>("h0"))
    reg Jotaro_stop_r : UInt<1>, clock with : 
      reset => (reset, UInt<1>("h0"))
    when _T_2 :
      io.Jotaro_stop <= UInt<1>("h1")
      Jotaro_stop_r <= UInt<1>("h1")
    else :
      io.Jotaro_stop <= Jotaro_stop_r
