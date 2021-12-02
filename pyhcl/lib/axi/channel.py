from pyhcl import *

"""
	// Read Address Channel
	addr_t araddr;
	logic arvalid;
	logic arready;

	// Read Data Channel
	data_t rdata;
	resp_t rresp;
	logic rvalid;
	logic rready;

	// Write Address Channel
	addr_t awaddr;
	logic awvalid;
	logic awready;

	// Write Data Channel
	data_t wdata;
	strb_t wstrb;
	logic wvalid;
	logic wready;

	// Write Response Channel
	resp_t bresp;
	logic bvalid;
	logic bready;
"""





class AxiIOFactory:
    @classmethod
    def make(cls, aw, dw, master=1):
        if master:
            axi = IO(
                # read addr channel
                ar=IO(
                    addr=Output(U.w(aw)),
                    vaild=Output(Bool),
                    ready=Input(Bool),
                ),
                # read data channel
                rd=IO(
                    data=Input(U.w(dw)),
                    resp=Input(Bool),
                    vaild=Input(Bool),
                    ready=Output(Bool),
                ),
                # addr write channel
                aw=IO(
                    addr=Output(U.w(aw)),
                    vaild=Output(Bool),
                    ready=Input(Bool),
                ),
                # write data channel
                wd=IO(
                    data=Output(U.w(dw)),
                    strb=Output(Bool),
                    vaild=Output(Bool),
                    ready=Input(Bool),
                ),
                # write resp channel
                wr=IO(
                    resp=Input(Bool),
                    valid=Input(Bool),
                    ready=Output(Bool),
                )
            )
        else:
            axi = IO(
                ar=IO(
                    addr=Input(U.w(aw)),
                    vaild=Input(Bool),
                    ready=Output(Bool),
                ),
                # read data channel
                rd=IO(
                    data=Output(U.w(dw)),
                    resp=Output(Bool),
                    vaild=Output(Bool),
                    ready=Input(Bool),
                ),
                # addr write channel
                aw=IO(
                    addr=Input(U.w(aw)),
                    vaild=Input(Bool),
                    ready=Output(Bool),
                ),
                # write data channel
                wd=IO(
                    data=Input(U.w(dw)),
                    strb=Input(Bool),
                    vaild=Input(Bool),
                    ready=Output(Bool),
                ),
                # write resp channel
                wr=IO(
                    resp=Output(Bool),
                    valid=Output(Bool),
                    ready=Input(Bool),
                )
            )

        return axi