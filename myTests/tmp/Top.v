module Top(
  input         clock,
  input         reset,
  input  [31:0] io_a,
  input  [31:0] io_b,
  output [31:0] io_c
);
  wire [32:0] _GEN_0 = io_a + io_b;
  assign io_c = _GEN_0[31:0];
endmodule
