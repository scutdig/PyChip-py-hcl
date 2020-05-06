// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Tracing implementation internals
#include "verilated_vcd_c.h"
#include "VAdder__Syms.h"


//======================

void VAdder::traceChg(VerilatedVcd* vcdp, void* userthis, uint32_t code) {
    // Callback from vcd->dump()
    VAdder* t = (VAdder*)userthis;
    VAdder__Syms* __restrict vlSymsp = t->__VlSymsp;  // Setup global symbol table
    if (vlSymsp->getClearActivity()) {
        t->traceChgThis(vlSymsp, vcdp, code);
    }
}

//======================


void VAdder::traceChgThis(VAdder__Syms* __restrict vlSymsp, VerilatedVcd* vcdp, uint32_t code) {
    VAdder* __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    int c=code;
    if (0 && vcdp && c) {}  // Prevent unused
    // Body
    {
        vlTOPp->traceChgThis__2(vlSymsp, vcdp, code);
    }
    // Final
    vlTOPp->__Vm_traceActivity = 0U;
}

void VAdder::traceChgThis__2(VAdder__Syms* __restrict vlSymsp, VerilatedVcd* vcdp, uint32_t code) {
    VAdder* __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    int c=code;
    if (0 && vcdp && c) {}  // Prevent unused
    // Body
    {
        vcdp->chgBit(c+1,(vlTOPp->clock));
        vcdp->chgBit(c+2,(vlTOPp->reset));
        vcdp->chgBus(c+3,(vlTOPp->io_a),8);
        vcdp->chgBus(c+4,(vlTOPp->io_b),8);
        vcdp->chgBit(c+5,(vlTOPp->io_cin));
        vcdp->chgBus(c+6,(vlTOPp->io_sum),8);
        vcdp->chgBit(c+7,(vlTOPp->io_cout));
        vcdp->chgBit(c+8,((1U & ((((IData)(vlTOPp->io_a) 
                                   ^ (IData)(vlTOPp->io_b)) 
                                  >> 7U) ^ (IData)(vlTOPp->Adder__DOT___T_18_io_cout)))));
        vcdp->chgBit(c+9,((1U & ((((IData)(vlTOPp->io_a) 
                                   ^ (IData)(vlTOPp->io_b)) 
                                  >> 6U) ^ (IData)(vlTOPp->Adder__DOT___T_15_io_cout)))));
        vcdp->chgBit(c+10,((1U & ((((IData)(vlTOPp->io_a) 
                                    ^ (IData)(vlTOPp->io_b)) 
                                   >> 5U) ^ (IData)(vlTOPp->Adder__DOT___T_12_io_cout)))));
        vcdp->chgBit(c+11,((1U & ((((IData)(vlTOPp->io_a) 
                                    ^ (IData)(vlTOPp->io_b)) 
                                   >> 4U) ^ (IData)(vlTOPp->Adder__DOT___T_9_io_cout)))));
        vcdp->chgBit(c+12,((1U & ((((IData)(vlTOPp->io_a) 
                                    ^ (IData)(vlTOPp->io_b)) 
                                   >> 3U) ^ (IData)(vlTOPp->Adder__DOT___T_6_io_cout)))));
        vcdp->chgBit(c+13,((1U & ((((IData)(vlTOPp->io_a) 
                                    ^ (IData)(vlTOPp->io_b)) 
                                   >> 2U) ^ (IData)(vlTOPp->Adder__DOT___T_3_io_cout)))));
        vcdp->chgBit(c+14,((1U & ((((IData)(vlTOPp->io_a) 
                                    ^ (IData)(vlTOPp->io_b)) 
                                   >> 1U) ^ (IData)(vlTOPp->Adder__DOT___T_io_cout)))));
        vcdp->chgBit(c+15,((1U & (((IData)(vlTOPp->io_a) 
                                   ^ (IData)(vlTOPp->io_b)) 
                                  ^ (IData)(vlTOPp->io_cin)))));
    }
}
