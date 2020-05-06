module FullAdder(
  input   clock,
  input   reset,
  input   io_a,
  input   io_b,
  input   io_cin,
  output  io_s,
  output  io_cout
);
  wire  _T;
  wire  _T_2;
  wire  _T_3;
  wire  _T_4;
  wire  _T_5;
  assign _T = io_a ^ io_b;
  assign _T_2 = io_a & io_b;
  assign _T_3 = io_a & io_cin;
  assign _T_4 = _T_2 | _T_3;
  assign _T_5 = io_b & io_cin;
  assign io_s = _T ^ io_cin;
  assign io_cout = _T_4 | _T_5;
endmodule
