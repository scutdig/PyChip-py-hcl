module FullAdder(
  input   io_a,
  input   io_b,
  input   io_cin,
  output  io_sum,
  output  io_cout
);
  wire  a_xor_b;
  wire  a_and_b;
  wire  b_and_cin;
  wire  _T_1;
  wire  a_and_cin;
  assign a_xor_b = io_a ^ io_b;
  assign a_and_b = io_a & io_b;
  assign b_and_cin = io_b & io_cin;
  assign _T_1 = a_and_b | b_and_cin;
  assign a_and_cin = io_a & io_cin;
  assign io_sum = a_xor_b ^ io_cin;
  assign io_cout = _T_1 | a_and_cin;
endmodule
module Adder(
  input        clock,
  input        reset,
  input  [7:0] io_a,
  input  [7:0] io_b,
  input        io_cin,
  output [7:0] io_sum,
  output       io_cout
);
  wire  _T_io_a;
  wire  _T_io_b;
  wire  _T_io_cin;
  wire  _T_io_sum;
  wire  _T_io_cout;
  wire  _T_3_io_a;
  wire  _T_3_io_b;
  wire  _T_3_io_cin;
  wire  _T_3_io_sum;
  wire  _T_3_io_cout;
  wire  _T_6_io_a;
  wire  _T_6_io_b;
  wire  _T_6_io_cin;
  wire  _T_6_io_sum;
  wire  _T_6_io_cout;
  wire  _T_9_io_a;
  wire  _T_9_io_b;
  wire  _T_9_io_cin;
  wire  _T_9_io_sum;
  wire  _T_9_io_cout;
  wire  _T_12_io_a;
  wire  _T_12_io_b;
  wire  _T_12_io_cin;
  wire  _T_12_io_sum;
  wire  _T_12_io_cout;
  wire  _T_15_io_a;
  wire  _T_15_io_b;
  wire  _T_15_io_cin;
  wire  _T_15_io_sum;
  wire  _T_15_io_cout;
  wire  _T_18_io_a;
  wire  _T_18_io_b;
  wire  _T_18_io_cin;
  wire  _T_18_io_sum;
  wire  _T_18_io_cout;
  wire  _T_21_io_a;
  wire  _T_21_io_b;
  wire  _T_21_io_cin;
  wire  _T_21_io_sum;
  wire  _T_21_io_cout;
  wire  sum_7;
  wire  sum_6;
  wire  sum_5;
  wire  sum_4;
  wire [3:0] _T_26;
  wire  sum_3;
  wire  sum_2;
  wire  sum_1;
  wire  sum_0;
  wire [3:0] _T_29;
  FullAdder _T (
    .io_a(_T_io_a),
    .io_b(_T_io_b),
    .io_cin(_T_io_cin),
    .io_sum(_T_io_sum),
    .io_cout(_T_io_cout)
  );
  FullAdder _T_3 (
    .io_a(_T_3_io_a),
    .io_b(_T_3_io_b),
    .io_cin(_T_3_io_cin),
    .io_sum(_T_3_io_sum),
    .io_cout(_T_3_io_cout)
  );
  FullAdder _T_6 (
    .io_a(_T_6_io_a),
    .io_b(_T_6_io_b),
    .io_cin(_T_6_io_cin),
    .io_sum(_T_6_io_sum),
    .io_cout(_T_6_io_cout)
  );
  FullAdder _T_9 (
    .io_a(_T_9_io_a),
    .io_b(_T_9_io_b),
    .io_cin(_T_9_io_cin),
    .io_sum(_T_9_io_sum),
    .io_cout(_T_9_io_cout)
  );
  FullAdder _T_12 (
    .io_a(_T_12_io_a),
    .io_b(_T_12_io_b),
    .io_cin(_T_12_io_cin),
    .io_sum(_T_12_io_sum),
    .io_cout(_T_12_io_cout)
  );
  FullAdder _T_15 (
    .io_a(_T_15_io_a),
    .io_b(_T_15_io_b),
    .io_cin(_T_15_io_cin),
    .io_sum(_T_15_io_sum),
    .io_cout(_T_15_io_cout)
  );
  FullAdder _T_18 (
    .io_a(_T_18_io_a),
    .io_b(_T_18_io_b),
    .io_cin(_T_18_io_cin),
    .io_sum(_T_18_io_sum),
    .io_cout(_T_18_io_cout)
  );
  FullAdder _T_21 (
    .io_a(_T_21_io_a),
    .io_b(_T_21_io_b),
    .io_cin(_T_21_io_cin),
    .io_sum(_T_21_io_sum),
    .io_cout(_T_21_io_cout)
  );
  assign sum_7 = _T_21_io_sum;
  assign sum_6 = _T_18_io_sum;
  assign sum_5 = _T_15_io_sum;
  assign sum_4 = _T_12_io_sum;
  assign _T_26 = {sum_7,sum_6,sum_5,sum_4};
  assign sum_3 = _T_9_io_sum;
  assign sum_2 = _T_6_io_sum;
  assign sum_1 = _T_3_io_sum;
  assign sum_0 = _T_io_sum;
  assign _T_29 = {sum_3,sum_2,sum_1,sum_0};
  assign io_sum = {_T_26,_T_29};
  assign io_cout = _T_21_io_cout;
  assign _T_io_a = io_a[0];
  assign _T_io_b = io_b[0];
  assign _T_io_cin = io_cin;
  assign _T_3_io_a = io_a[1];
  assign _T_3_io_b = io_b[1];
  assign _T_3_io_cin = _T_io_cout;
  assign _T_6_io_a = io_a[2];
  assign _T_6_io_b = io_b[2];
  assign _T_6_io_cin = _T_3_io_cout;
  assign _T_9_io_a = io_a[3];
  assign _T_9_io_b = io_b[3];
  assign _T_9_io_cin = _T_6_io_cout;
  assign _T_12_io_a = io_a[4];
  assign _T_12_io_b = io_b[4];
  assign _T_12_io_cin = _T_9_io_cout;
  assign _T_15_io_a = io_a[5];
  assign _T_15_io_b = io_b[5];
  assign _T_15_io_cin = _T_12_io_cout;
  assign _T_18_io_a = io_a[6];
  assign _T_18_io_b = io_b[6];
  assign _T_18_io_cin = _T_15_io_cout;
  assign _T_21_io_a = io_a[7];
  assign _T_21_io_b = io_b[7];
  assign _T_21_io_cin = _T_18_io_cout;
endmodule
