module Test(
  input   clock,
  input   reset,
  output  io_DIO_stop,
  output  io_Jotaro_stop
);
  reg [31:0] counter;
  reg [31:0] _RAND_0;
  wire [32:0] _T;
  wire  _T_1;
  reg  DIO_stop_r;
  reg [31:0] _RAND_1;
  wire  _GEN_0;
  wire  _T_2;
  reg  Jotaro_stop_r;
  reg [31:0] _RAND_2;
  wire  _GEN_2;
  assign _T = counter + 32'h1;
  assign _T_1 = counter == 32'ha;
  assign _GEN_0 = _T_1 ? 1'h0 : DIO_stop_r;
  assign _T_2 = io_DIO_stop == 1'h0;
  assign _GEN_2 = _T_2 | Jotaro_stop_r;
  assign io_DIO_stop = _T_1 ? 1'h0 : DIO_stop_r;
  assign io_Jotaro_stop = _T_2 | Jotaro_stop_r;
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
  counter = _RAND_0[31:0];
  `endif // RANDOMIZE_REG_INIT
  `ifdef RANDOMIZE_REG_INIT
  _RAND_1 = {1{`RANDOM}};
  DIO_stop_r = _RAND_1[0:0];
  `endif // RANDOMIZE_REG_INIT
  `ifdef RANDOMIZE_REG_INIT
  _RAND_2 = {1{`RANDOM}};
  Jotaro_stop_r = _RAND_2[0:0];
  `endif // RANDOMIZE_REG_INIT
  `endif // RANDOMIZE
end // initial
`endif // SYNTHESIS
  always @(posedge clock) begin
    if (reset) begin
      counter <= 32'h0;
    end else begin
      counter <= _T[31:0];
    end
    DIO_stop_r <= reset | _GEN_0;
    if (reset) begin
      Jotaro_stop_r <= 1'h0;
    end else begin
      Jotaro_stop_r <= _GEN_2;
    end
  end
endmodule
