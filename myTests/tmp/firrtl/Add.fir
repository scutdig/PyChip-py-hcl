module Add :
    input in1 : UInt<32>
    input in2 : UInt<32>
    output out : UInt<32>
    out <= add(in1, in2)