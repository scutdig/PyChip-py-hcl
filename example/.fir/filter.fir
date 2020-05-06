circuit MyManyDynamicElementVecFir :
  module MyManyDynamicElementVecFir :
    input clock : Clock
    input reset : UInt<1>
    output io : {flip i : UInt<8>, flip valid : UInt<1>, o : UInt<8>}
  
    reg _T : UInt<8>, clock with : 
      reset => (reset, UInt<8>("h0"))
    when io.valid :
      _T <= io.i
    reg _T_1 : UInt<8>, clock with : 
      reset => (reset, UInt<8>("h0"))
    when io.valid :
      _T_1 <= _T
    reg a : UInt<8>, clock with : 
      reset => (reset, UInt<8>("h0"))
    when io.valid :
      a <= _T_1
    reg b : UInt<8>, clock with : 
      reset => (reset, UInt<8>("h0"))
    when io.valid :
      b <= a
    node _T_2 = mul(io.i, UInt<1>("h0"))
    node _T_3 = mul(_T, UInt<1>("h1"))
    node _T_4 = add(_T_2, _T_3)
    node _T_5 = mul(_T_1, UInt<2>("h2"))
    node _T_6 = add(_T_4, _T_5)
    node _T_7 = mul(a, UInt<2>("h3"))
    node _T_8 = add(_T_6, _T_7)
    io.o <= bits(_T_8, 7, 0)
