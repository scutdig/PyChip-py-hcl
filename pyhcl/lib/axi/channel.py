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


class IOFactory:
    @classmethod
    def make(cls, **ios):
        return IO(ios)


class AxiIOFactory:
    @classmethod
    def make(cls, aw, dw, master=1):
        axilite_ios = {}

        if master:
            axilite_ios = {
                # read addr channel
                "araddr": Output(U.w(aw)),
                "arvaild": Output(Bool),
                "arready": Input(Bool),
                # read data channel
                "rdata": Input(U.w(dw)),
                "rresp": Input(Bool),
                "rvaild": Input(Bool),
                "rready": Output(Bool),
                # addr write channel
                "awaddr": Output(U.w(aw)),
                "awvaild": Output(Bool),
                "awready": Input(Bool),
                # write data channel
                "wdata": Output(U.w(dw)),
                "wstrb": Output(Bool),
                "wvaild": Output(Bool),
                "wready": Input(Bool),
                # write resp channel
                "bresp": Input(Bool),
                "bvalid": Input(Bool),
                "bready": Output(Bool),
            }
        else:
            axilite_ios = {
                # addr read channel
                "araddr": Input(U.w(aw)),
                "arvaild": Input(Bool),
                "arready": Output(Bool),
                # read data channel
                "rdata": Output(U.w(dw)),
                "rresp": Output(Bool),
                "rvaild": Output(Bool),
                "rready": Input(Bool),
                # write addr channel
                "awaddr": Input(U.w(aw)),
                "awvaild": Input(Bool),
                "awready": Output(Bool),
                # write data channel
                "wdata": Input(U.w(dw)),
                "wstrb": Input(Bool),
                "wvaild": Input(Bool),
                "wready": Output(Bool),
                # write resp channel
                "bresp": Output(Bool),
                "bvalid": Output(Bool),
                "bready": Input(Bool),
            }

        return IOFactory.make(axilite_ios)
