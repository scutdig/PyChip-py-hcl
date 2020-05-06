module MyManyDynamicElementVecFir(
  input        clock,
  input        reset,
  input  [7:0] io_i,
  input        io_valid,
  output [7:0] io_o
);
  reg [7:0] _T;
  reg [31:0] _RAND_0;
  reg [7:0] _T_1;
  reg [31:0] _RAND_1;
  reg [7:0] a;
  reg [31:0] _RAND_2;
  wire [8:0] _T_2;
  wire [8:0] _T_3;
  wire [9:0] _T_4;
  wire [9:0] _T_5;
  wire [10:0] _T_6;
  wire [9:0] _T_7;
  wire [10:0] _GEN_4;
  wire [11:0] _T_8;
  assign _T_2 = io_i * 8'h0;
  assign _T_3 = _T * 8'h1;
  assign _T_4 = _T_2 + _T_3;
  assign _T_5 = _T_1 * 8'h2;
  assign _T_6 = _T_4 + _T_5;
  assign _T_7 = a * 8'h3;
  assign _GEN_4 = {{1'd0}, _T_7};
  assign _T_8 = _T_6 + _GEN_4;
  assign io_o = _T_8[7:0];
`ifdef RANDOMIZE_GARBAGE_ASSIGN
`define RANDOMIZE
`endif
`ifdef RANDOMIZE_INVALID_ASSIGN
`define RANDOMIZE
`endif
`ifdef RANDOMIZE_REG_INIT
`define RANDOMIZE
`endif
`ifdef RANDOMIZE_MEM_INIT
`define RANDOMIZE
`endif
`ifndef RANDOM
`define RANDOM $random
`endif
`ifdef RANDOMIZE_MEM_INIT
  integer initvar;
`endif
`ifndef SYNTHESIS
initial begin
  `ifdef RANDOMIZE
    `ifdef INIT_RANDOM
      `INIT_RANDOM
    `endif
    `ifndef VERILATOR
      `ifdef RANDOMIZE_DELAY
        #`RANDOMIZE_DELAY begin end
      `else
        #0.002 begin end
      `endif
    `endif
  `ifdef RANDOMIZE_REG_INIT
  _RAND_0 = {1{`RANDOM}};
  _T = _RAND_0[7:0];
  `endif // RANDOMIZE_REG_INIT
  `ifdef RANDOMIZE_REG_INIT
  _RAND_1 = {1{`RANDOM}};
  _T_1 = _RAND_1[7:0];
  `endif // RANDOMIZE_REG_INIT
  `ifdef RANDOMIZE_REG_INIT
  _RAND_2 = {1{`RANDOM}};
  a = _RAND_2[7:0];
  `endif // RANDOMIZE_REG_INIT
  `endif // RANDOMIZE
end // initial
`endif // SYNTHESIS
  always @(posedge clock) begin
    if (reset) begin
      _T <= 8'h0;
    end else if (io_valid) begin
      _T <= io_i;
    end
    if (reset) begin
      _T_1 <= 8'h0;
    end else if (io_valid) begin
      _T_1 <= _T;
    end
    if (reset) begin
      a <= 8'h0;
    end else if (io_valid) begin
      a <= _T_1;
    end
  end
endmodule
