module Top(
  input  clock,
  input  reset,
  input  [31:0] io_a,
  input  [31:0] io_b,
  output [31:0] io_c

);
  wire [31:0] add_in1;
  wire [31:0] add_in2;
  wire [31:0] add_out;
  Add add (
    .in1(add_in1),
    .in2(add_in2),
    .out(add_out)
  );
  assign io_c = add_out;
  assign add_in1 = io_a;
  assign add_in2 = io_b;
endmodule
