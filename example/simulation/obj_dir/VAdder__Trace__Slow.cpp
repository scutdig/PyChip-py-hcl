// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Tracing implementation internals
#include "verilated_vcd_c.h"
#include "VAdder__Syms.h"


//======================

void VAdder::trace(VerilatedVcdC* tfp, int, int) {
    tfp->spTrace()->addCallback(&VAdder::traceInit, &VAdder::traceFull, &VAdder::traceChg, this);
}
void VAdder::traceInit(VerilatedVcd* vcdp, void* userthis, uint32_t code) {
    // Callback from vcd->open()
    VAdder* t = (VAdder*)userthis;
    VAdder__Syms* __restrict vlSymsp = t->__VlSymsp;  // Setup global symbol table
    if (!Verilated::calcUnusedSigs()) {
        VL_FATAL_MT(__FILE__,__LINE__,__FILE__,"Turning on wave traces requires Verilated::traceEverOn(true) call before time 0.");
    }
    vcdp->scopeEscape(' ');
    t->traceInitThis(vlSymsp, vcdp, code);
    vcdp->scopeEscape('.');
}
void VAdder::traceFull(VerilatedVcd* vcdp, void* userthis, uint32_t code) {
    // Callback from vcd->dump()
    VAdder* t = (VAdder*)userthis;
    VAdder__Syms* __restrict vlSymsp = t->__VlSymsp;  // Setup global symbol table
    t->traceFullThis(vlSymsp, vcdp, code);
}

//======================


void VAdder::traceInitThis(VAdder__Syms* __restrict vlSymsp, VerilatedVcd* vcdp, uint32_t code) {
    VAdder* __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    int c=code;
    if (0 && vcdp && c) {}  // Prevent unused
    vcdp->module(vlSymsp->name());  // Setup signal names
    // Body
    {
        vlTOPp->traceInitThis__1(vlSymsp, vcdp, code);
    }
}

void VAdder::traceFullThis(VAdder__Syms* __restrict vlSymsp, VerilatedVcd* vcdp, uint32_t code) {
    VAdder* __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    int c=code;
    if (0 && vcdp && c) {}  // Prevent unused
    // Body
    {
        vlTOPp->traceFullThis__1(vlSymsp, vcdp, code);
    }
    // Final
    vlTOPp->__Vm_traceActivity = 0U;
}

void VAdder::traceInitThis__1(VAdder__Syms* __restrict vlSymsp, VerilatedVcd* vcdp, uint32_t code) {
    VAdder* __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    int c=code;
    if (0 && vcdp && c) {}  // Prevent unused
    // Body
    {
        vcdp->declBit(c+1,"clock",-1);
        vcdp->declBit(c+2,"reset",-1);
        vcdp->declBus(c+3,"io_a",-1,7,0);
        vcdp->declBus(c+4,"io_b",-1,7,0);
        vcdp->declBit(c+5,"io_cin",-1);
        vcdp->declBus(c+6,"io_sum",-1,7,0);
        vcdp->declBit(c+7,"io_cout",-1);
        vcdp->declBit(c+1,"Adder clock",-1);
        vcdp->declBit(c+2,"Adder reset",-1);
        vcdp->declBus(c+3,"Adder io_a",-1,7,0);
        vcdp->declBus(c+4,"Adder io_b",-1,7,0);
        vcdp->declBit(c+5,"Adder io_cin",-1);
        vcdp->declBus(c+6,"Adder io_sum",-1,7,0);
        vcdp->declBit(c+7,"Adder io_cout",-1);
        // Tracing: Adder _T_io_a // Ignored: Inlined leading underscore at Adder.v:30
        // Tracing: Adder _T_io_b // Ignored: Inlined leading underscore at Adder.v:31
        // Tracing: Adder _T_io_cin // Ignored: Inlined leading underscore at Adder.v:32
        // Tracing: Adder _T_io_sum // Ignored: Inlined leading underscore at Adder.v:33
        // Tracing: Adder _T_io_cout // Ignored: Inlined leading underscore at Adder.v:34
        // Tracing: Adder _T_3_io_a // Ignored: Inlined leading underscore at Adder.v:35
        // Tracing: Adder _T_3_io_b // Ignored: Inlined leading underscore at Adder.v:36
        // Tracing: Adder _T_3_io_cin // Ignored: Inlined leading underscore at Adder.v:37
        // Tracing: Adder _T_3_io_sum // Ignored: Inlined leading underscore at Adder.v:38
        // Tracing: Adder _T_3_io_cout // Ignored: Inlined leading underscore at Adder.v:39
        // Tracing: Adder _T_6_io_a // Ignored: Inlined leading underscore at Adder.v:40
        // Tracing: Adder _T_6_io_b // Ignored: Inlined leading underscore at Adder.v:41
        // Tracing: Adder _T_6_io_cin // Ignored: Inlined leading underscore at Adder.v:42
        // Tracing: Adder _T_6_io_sum // Ignored: Inlined leading underscore at Adder.v:43
        // Tracing: Adder _T_6_io_cout // Ignored: Inlined leading underscore at Adder.v:44
        // Tracing: Adder _T_9_io_a // Ignored: Inlined leading underscore at Adder.v:45
        // Tracing: Adder _T_9_io_b // Ignored: Inlined leading underscore at Adder.v:46
        // Tracing: Adder _T_9_io_cin // Ignored: Inlined leading underscore at Adder.v:47
        // Tracing: Adder _T_9_io_sum // Ignored: Inlined leading underscore at Adder.v:48
        // Tracing: Adder _T_9_io_cout // Ignored: Inlined leading underscore at Adder.v:49
        // Tracing: Adder _T_12_io_a // Ignored: Inlined leading underscore at Adder.v:50
        // Tracing: Adder _T_12_io_b // Ignored: Inlined leading underscore at Adder.v:51
        // Tracing: Adder _T_12_io_cin // Ignored: Inlined leading underscore at Adder.v:52
        // Tracing: Adder _T_12_io_sum // Ignored: Inlined leading underscore at Adder.v:53
        // Tracing: Adder _T_12_io_cout // Ignored: Inlined leading underscore at Adder.v:54
        // Tracing: Adder _T_15_io_a // Ignored: Inlined leading underscore at Adder.v:55
        // Tracing: Adder _T_15_io_b // Ignored: Inlined leading underscore at Adder.v:56
        // Tracing: Adder _T_15_io_cin // Ignored: Inlined leading underscore at Adder.v:57
        // Tracing: Adder _T_15_io_sum // Ignored: Inlined leading underscore at Adder.v:58
        // Tracing: Adder _T_15_io_cout // Ignored: Inlined leading underscore at Adder.v:59
        // Tracing: Adder _T_18_io_a // Ignored: Inlined leading underscore at Adder.v:60
        // Tracing: Adder _T_18_io_b // Ignored: Inlined leading underscore at Adder.v:61
        // Tracing: Adder _T_18_io_cin // Ignored: Inlined leading underscore at Adder.v:62
        // Tracing: Adder _T_18_io_sum // Ignored: Inlined leading underscore at Adder.v:63
        // Tracing: Adder _T_18_io_cout // Ignored: Inlined leading underscore at Adder.v:64
        // Tracing: Adder _T_21_io_a // Ignored: Inlined leading underscore at Adder.v:65
        // Tracing: Adder _T_21_io_b // Ignored: Inlined leading underscore at Adder.v:66
        // Tracing: Adder _T_21_io_cin // Ignored: Inlined leading underscore at Adder.v:67
        // Tracing: Adder _T_21_io_sum // Ignored: Inlined leading underscore at Adder.v:68
        // Tracing: Adder _T_21_io_cout // Ignored: Inlined leading underscore at Adder.v:69
        vcdp->declBit(c+8,"Adder sum_7",-1);
        vcdp->declBit(c+9,"Adder sum_6",-1);
        vcdp->declBit(c+10,"Adder sum_5",-1);
        vcdp->declBit(c+11,"Adder sum_4",-1);
        // Tracing: Adder _T_26 // Ignored: Inlined leading underscore at Adder.v:74
        vcdp->declBit(c+12,"Adder sum_3",-1);
        vcdp->declBit(c+13,"Adder sum_2",-1);
        vcdp->declBit(c+14,"Adder sum_1",-1);
        vcdp->declBit(c+15,"Adder sum_0",-1);
        // Tracing: Adder _T_29 // Ignored: Inlined leading underscore at Adder.v:79
        // Tracing: Adder _T io_a // Ignored: Inlined leading underscore at Adder.v:2
        // Tracing: Adder _T io_b // Ignored: Inlined leading underscore at Adder.v:3
        // Tracing: Adder _T io_cin // Ignored: Inlined leading underscore at Adder.v:4
        // Tracing: Adder _T io_sum // Ignored: Inlined leading underscore at Adder.v:5
        // Tracing: Adder _T io_cout // Ignored: Inlined leading underscore at Adder.v:6
        // Tracing: Adder _T a_xor_b // Ignored: Inlined leading underscore at Adder.v:8
        // Tracing: Adder _T a_and_b // Ignored: Inlined leading underscore at Adder.v:9
        // Tracing: Adder _T b_and_cin // Ignored: Inlined leading underscore at Adder.v:10
        // Tracing: Adder _T _T_1 // Ignored: Inlined leading underscore at Adder.v:11
        // Tracing: Adder _T a_and_cin // Ignored: Inlined leading underscore at Adder.v:12
        // Tracing: Adder _T_3 io_a // Ignored: Inlined leading underscore at Adder.v:2
        // Tracing: Adder _T_3 io_b // Ignored: Inlined leading underscore at Adder.v:3
        // Tracing: Adder _T_3 io_cin // Ignored: Inlined leading underscore at Adder.v:4
        // Tracing: Adder _T_3 io_sum // Ignored: Inlined leading underscore at Adder.v:5
        // Tracing: Adder _T_3 io_cout // Ignored: Inlined leading underscore at Adder.v:6
        // Tracing: Adder _T_3 a_xor_b // Ignored: Inlined leading underscore at Adder.v:8
        // Tracing: Adder _T_3 a_and_b // Ignored: Inlined leading underscore at Adder.v:9
        // Tracing: Adder _T_3 b_and_cin // Ignored: Inlined leading underscore at Adder.v:10
        // Tracing: Adder _T_3 _T_1 // Ignored: Inlined leading underscore at Adder.v:11
        // Tracing: Adder _T_3 a_and_cin // Ignored: Inlined leading underscore at Adder.v:12
        // Tracing: Adder _T_6 io_a // Ignored: Inlined leading underscore at Adder.v:2
        // Tracing: Adder _T_6 io_b // Ignored: Inlined leading underscore at Adder.v:3
        // Tracing: Adder _T_6 io_cin // Ignored: Inlined leading underscore at Adder.v:4
        // Tracing: Adder _T_6 io_sum // Ignored: Inlined leading underscore at Adder.v:5
        // Tracing: Adder _T_6 io_cout // Ignored: Inlined leading underscore at Adder.v:6
        // Tracing: Adder _T_6 a_xor_b // Ignored: Inlined leading underscore at Adder.v:8
        // Tracing: Adder _T_6 a_and_b // Ignored: Inlined leading underscore at Adder.v:9
        // Tracing: Adder _T_6 b_and_cin // Ignored: Inlined leading underscore at Adder.v:10
        // Tracing: Adder _T_6 _T_1 // Ignored: Inlined leading underscore at Adder.v:11
        // Tracing: Adder _T_6 a_and_cin // Ignored: Inlined leading underscore at Adder.v:12
        // Tracing: Adder _T_9 io_a // Ignored: Inlined leading underscore at Adder.v:2
        // Tracing: Adder _T_9 io_b // Ignored: Inlined leading underscore at Adder.v:3
        // Tracing: Adder _T_9 io_cin // Ignored: Inlined leading underscore at Adder.v:4
        // Tracing: Adder _T_9 io_sum // Ignored: Inlined leading underscore at Adder.v:5
        // Tracing: Adder _T_9 io_cout // Ignored: Inlined leading underscore at Adder.v:6
        // Tracing: Adder _T_9 a_xor_b // Ignored: Inlined leading underscore at Adder.v:8
        // Tracing: Adder _T_9 a_and_b // Ignored: Inlined leading underscore at Adder.v:9
        // Tracing: Adder _T_9 b_and_cin // Ignored: Inlined leading underscore at Adder.v:10
        // Tracing: Adder _T_9 _T_1 // Ignored: Inlined leading underscore at Adder.v:11
        // Tracing: Adder _T_9 a_and_cin // Ignored: Inlined leading underscore at Adder.v:12
        // Tracing: Adder _T_12 io_a // Ignored: Inlined leading underscore at Adder.v:2
        // Tracing: Adder _T_12 io_b // Ignored: Inlined leading underscore at Adder.v:3
        // Tracing: Adder _T_12 io_cin // Ignored: Inlined leading underscore at Adder.v:4
        // Tracing: Adder _T_12 io_sum // Ignored: Inlined leading underscore at Adder.v:5
        // Tracing: Adder _T_12 io_cout // Ignored: Inlined leading underscore at Adder.v:6
        // Tracing: Adder _T_12 a_xor_b // Ignored: Inlined leading underscore at Adder.v:8
        // Tracing: Adder _T_12 a_and_b // Ignored: Inlined leading underscore at Adder.v:9
        // Tracing: Adder _T_12 b_and_cin // Ignored: Inlined leading underscore at Adder.v:10
        // Tracing: Adder _T_12 _T_1 // Ignored: Inlined leading underscore at Adder.v:11
        // Tracing: Adder _T_12 a_and_cin // Ignored: Inlined leading underscore at Adder.v:12
        // Tracing: Adder _T_15 io_a // Ignored: Inlined leading underscore at Adder.v:2
        // Tracing: Adder _T_15 io_b // Ignored: Inlined leading underscore at Adder.v:3
        // Tracing: Adder _T_15 io_cin // Ignored: Inlined leading underscore at Adder.v:4
        // Tracing: Adder _T_15 io_sum // Ignored: Inlined leading underscore at Adder.v:5
        // Tracing: Adder _T_15 io_cout // Ignored: Inlined leading underscore at Adder.v:6
        // Tracing: Adder _T_15 a_xor_b // Ignored: Inlined leading underscore at Adder.v:8
        // Tracing: Adder _T_15 a_and_b // Ignored: Inlined leading underscore at Adder.v:9
        // Tracing: Adder _T_15 b_and_cin // Ignored: Inlined leading underscore at Adder.v:10
        // Tracing: Adder _T_15 _T_1 // Ignored: Inlined leading underscore at Adder.v:11
        // Tracing: Adder _T_15 a_and_cin // Ignored: Inlined leading underscore at Adder.v:12
        // Tracing: Adder _T_18 io_a // Ignored: Inlined leading underscore at Adder.v:2
        // Tracing: Adder _T_18 io_b // Ignored: Inlined leading underscore at Adder.v:3
        // Tracing: Adder _T_18 io_cin // Ignored: Inlined leading underscore at Adder.v:4
        // Tracing: Adder _T_18 io_sum // Ignored: Inlined leading underscore at Adder.v:5
        // Tracing: Adder _T_18 io_cout // Ignored: Inlined leading underscore at Adder.v:6
        // Tracing: Adder _T_18 a_xor_b // Ignored: Inlined leading underscore at Adder.v:8
        // Tracing: Adder _T_18 a_and_b // Ignored: Inlined leading underscore at Adder.v:9
        // Tracing: Adder _T_18 b_and_cin // Ignored: Inlined leading underscore at Adder.v:10
        // Tracing: Adder _T_18 _T_1 // Ignored: Inlined leading underscore at Adder.v:11
        // Tracing: Adder _T_18 a_and_cin // Ignored: Inlined leading underscore at Adder.v:12
        // Tracing: Adder _T_21 io_a // Ignored: Inlined leading underscore at Adder.v:2
        // Tracing: Adder _T_21 io_b // Ignored: Inlined leading underscore at Adder.v:3
        // Tracing: Adder _T_21 io_cin // Ignored: Inlined leading underscore at Adder.v:4
        // Tracing: Adder _T_21 io_sum // Ignored: Inlined leading underscore at Adder.v:5
        // Tracing: Adder _T_21 io_cout // Ignored: Inlined leading underscore at Adder.v:6
        // Tracing: Adder _T_21 a_xor_b // Ignored: Inlined leading underscore at Adder.v:8
        // Tracing: Adder _T_21 a_and_b // Ignored: Inlined leading underscore at Adder.v:9
        // Tracing: Adder _T_21 b_and_cin // Ignored: Inlined leading underscore at Adder.v:10
        // Tracing: Adder _T_21 _T_1 // Ignored: Inlined leading underscore at Adder.v:11
        // Tracing: Adder _T_21 a_and_cin // Ignored: Inlined leading underscore at Adder.v:12
    }
}

void VAdder::traceFullThis__1(VAdder__Syms* __restrict vlSymsp, VerilatedVcd* vcdp, uint32_t code) {
    VAdder* __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    int c=code;
    if (0 && vcdp && c) {}  // Prevent unused
    // Body
    {
        vcdp->fullBit(c+1,(vlTOPp->clock));
        vcdp->fullBit(c+2,(vlTOPp->reset));
        vcdp->fullBus(c+3,(vlTOPp->io_a),8);
        vcdp->fullBus(c+4,(vlTOPp->io_b),8);
        vcdp->fullBit(c+5,(vlTOPp->io_cin));
        vcdp->fullBus(c+6,(vlTOPp->io_sum),8);
        vcdp->fullBit(c+7,(vlTOPp->io_cout));
        vcdp->fullBit(c+8,((1U & ((((IData)(vlTOPp->io_a) 
                                    ^ (IData)(vlTOPp->io_b)) 
                                   >> 7U) ^ (IData)(vlTOPp->Adder__DOT___T_18_io_cout)))));
        vcdp->fullBit(c+9,((1U & ((((IData)(vlTOPp->io_a) 
                                    ^ (IData)(vlTOPp->io_b)) 
                                   >> 6U) ^ (IData)(vlTOPp->Adder__DOT___T_15_io_cout)))));
        vcdp->fullBit(c+10,((1U & ((((IData)(vlTOPp->io_a) 
                                     ^ (IData)(vlTOPp->io_b)) 
                                    >> 5U) ^ (IData)(vlTOPp->Adder__DOT___T_12_io_cout)))));
        vcdp->fullBit(c+11,((1U & ((((IData)(vlTOPp->io_a) 
                                     ^ (IData)(vlTOPp->io_b)) 
                                    >> 4U) ^ (IData)(vlTOPp->Adder__DOT___T_9_io_cout)))));
        vcdp->fullBit(c+12,((1U & ((((IData)(vlTOPp->io_a) 
                                     ^ (IData)(vlTOPp->io_b)) 
                                    >> 3U) ^ (IData)(vlTOPp->Adder__DOT___T_6_io_cout)))));
        vcdp->fullBit(c+13,((1U & ((((IData)(vlTOPp->io_a) 
                                     ^ (IData)(vlTOPp->io_b)) 
                                    >> 2U) ^ (IData)(vlTOPp->Adder__DOT___T_3_io_cout)))));
        vcdp->fullBit(c+14,((1U & ((((IData)(vlTOPp->io_a) 
                                     ^ (IData)(vlTOPp->io_b)) 
                                    >> 1U) ^ (IData)(vlTOPp->Adder__DOT___T_io_cout)))));
        vcdp->fullBit(c+15,((1U & (((IData)(vlTOPp->io_a) 
                                    ^ (IData)(vlTOPp->io_b)) 
                                   ^ (IData)(vlTOPp->io_cin)))));
    }
}
