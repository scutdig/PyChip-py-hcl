// Pysv
module Add(
	input [31:0]		in1 ,
	input [31:0]		in2 ,

	output [31:0]		out 
	);
	wire [31:0]	__tmp_in1 ;
	wire [31:0]	__tmp_in2 ;

	reg [31:0]	__tmp_out ;

	assign __tmp_in1 = in1 ;
	assign __tmp_in2 = in2 ;


	import pysv::* ;
	always begin
		fn(__tmp_in1, __tmp_in2, __tmp_out) ;
	end
	assign out = __tmp_out ;

endmodule
