// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See VAdder.h for the primary calling header

#include "VAdder.h"
#include "VAdder__Syms.h"


//--------------------
// STATIC VARIABLES


//--------------------

VL_CTOR_IMP(VAdder) {
    VAdder__Syms* __restrict vlSymsp = __VlSymsp = new VAdder__Syms(this, name());
    VAdder* __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    // Reset internal values
    
    // Reset structure values
    _ctor_var_reset();
}

void VAdder::__Vconfigure(VAdder__Syms* vlSymsp, bool first) {
    if (0 && first) {}  // Prevent unused
    this->__VlSymsp = vlSymsp;
}

VAdder::~VAdder() {
    delete __VlSymsp; __VlSymsp=NULL;
}

//--------------------


void VAdder::eval() {
    VL_DEBUG_IF(VL_DBG_MSGF("+++++TOP Evaluate VAdder::eval\n"); );
    VAdder__Syms* __restrict vlSymsp = this->__VlSymsp;  // Setup global symbol table
    VAdder* __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
#ifdef VL_DEBUG
    // Debug assertions
    _eval_debug_assertions();
#endif  // VL_DEBUG
    // Initialize
    if (VL_UNLIKELY(!vlSymsp->__Vm_didInit)) _eval_initial_loop(vlSymsp);
    // Evaluate till stable
    int __VclockLoop = 0;
    QData __Vchange = 1;
    do {
        VL_DEBUG_IF(VL_DBG_MSGF("+ Clock loop\n"););
        vlSymsp->__Vm_activity = true;
        _eval(vlSymsp);
        if (VL_UNLIKELY(++__VclockLoop > 100)) {
            // About to fail, so enable debug to see what's not settling.
            // Note you must run make with OPT=-DVL_DEBUG for debug prints.
            int __Vsaved_debug = Verilated::debug();
            Verilated::debug(1);
            __Vchange = _change_request(vlSymsp);
            Verilated::debug(__Vsaved_debug);
            VL_FATAL_MT(__FILE__,__LINE__,__FILE__,"Verilated model didn't converge");
        } else {
            __Vchange = _change_request(vlSymsp);
        }
    } while (VL_UNLIKELY(__Vchange));
}

void VAdder::_eval_initial_loop(VAdder__Syms* __restrict vlSymsp) {
    vlSymsp->__Vm_didInit = true;
    _eval_initial(vlSymsp);
    vlSymsp->__Vm_activity = true;
    // Evaluate till stable
    int __VclockLoop = 0;
    QData __Vchange = 1;
    do {
        _eval_settle(vlSymsp);
        _eval(vlSymsp);
        if (VL_UNLIKELY(++__VclockLoop > 100)) {
            // About to fail, so enable debug to see what's not settling.
            // Note you must run make with OPT=-DVL_DEBUG for debug prints.
            int __Vsaved_debug = Verilated::debug();
            Verilated::debug(1);
            __Vchange = _change_request(vlSymsp);
            Verilated::debug(__Vsaved_debug);
            VL_FATAL_MT(__FILE__,__LINE__,__FILE__,"Verilated model didn't DC converge");
        } else {
            __Vchange = _change_request(vlSymsp);
        }
    } while (VL_UNLIKELY(__Vchange));
}

//--------------------
// Internal Methods

VL_INLINE_OPT void VAdder::_combo__TOP__1(VAdder__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VAdder::_combo__TOP__1\n"); );
    VAdder* __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    // Body
    vlTOPp->Adder__DOT___T_io_cout = (1U & ((((IData)(vlTOPp->io_a) 
                                              & (IData)(vlTOPp->io_b)) 
                                             | ((IData)(vlTOPp->io_b) 
                                                & (IData)(vlTOPp->io_cin))) 
                                            | ((IData)(vlTOPp->io_a) 
                                               & (IData)(vlTOPp->io_cin))));
    vlTOPp->Adder__DOT___T_3_io_cout = (1U & (((((IData)(vlTOPp->io_a) 
                                                 & (IData)(vlTOPp->io_b)) 
                                                >> 1U) 
                                               | (((IData)(vlTOPp->io_b) 
                                                   >> 1U) 
                                                  & (IData)(vlTOPp->Adder__DOT___T_io_cout))) 
                                              | (((IData)(vlTOPp->io_a) 
                                                  >> 1U) 
                                                 & (IData)(vlTOPp->Adder__DOT___T_io_cout))));
    vlTOPp->Adder__DOT___T_6_io_cout = (1U & (((((IData)(vlTOPp->io_a) 
                                                 & (IData)(vlTOPp->io_b)) 
                                                >> 2U) 
                                               | (((IData)(vlTOPp->io_b) 
                                                   >> 2U) 
                                                  & (IData)(vlTOPp->Adder__DOT___T_3_io_cout))) 
                                              | (((IData)(vlTOPp->io_a) 
                                                  >> 2U) 
                                                 & (IData)(vlTOPp->Adder__DOT___T_3_io_cout))));
    vlTOPp->Adder__DOT___T_9_io_cout = (1U & (((((IData)(vlTOPp->io_a) 
                                                 & (IData)(vlTOPp->io_b)) 
                                                >> 3U) 
                                               | (((IData)(vlTOPp->io_b) 
                                                   >> 3U) 
                                                  & (IData)(vlTOPp->Adder__DOT___T_6_io_cout))) 
                                              | (((IData)(vlTOPp->io_a) 
                                                  >> 3U) 
                                                 & (IData)(vlTOPp->Adder__DOT___T_6_io_cout))));
    vlTOPp->Adder__DOT___T_12_io_cout = (1U & (((((IData)(vlTOPp->io_a) 
                                                  & (IData)(vlTOPp->io_b)) 
                                                 >> 4U) 
                                                | (((IData)(vlTOPp->io_b) 
                                                    >> 4U) 
                                                   & (IData)(vlTOPp->Adder__DOT___T_9_io_cout))) 
                                               | (((IData)(vlTOPp->io_a) 
                                                   >> 4U) 
                                                  & (IData)(vlTOPp->Adder__DOT___T_9_io_cout))));
    vlTOPp->Adder__DOT___T_15_io_cout = (1U & (((((IData)(vlTOPp->io_a) 
                                                  & (IData)(vlTOPp->io_b)) 
                                                 >> 5U) 
                                                | (((IData)(vlTOPp->io_b) 
                                                    >> 5U) 
                                                   & (IData)(vlTOPp->Adder__DOT___T_12_io_cout))) 
                                               | (((IData)(vlTOPp->io_a) 
                                                   >> 5U) 
                                                  & (IData)(vlTOPp->Adder__DOT___T_12_io_cout))));
    vlTOPp->Adder__DOT___T_18_io_cout = (1U & (((((IData)(vlTOPp->io_a) 
                                                  & (IData)(vlTOPp->io_b)) 
                                                 >> 6U) 
                                                | (((IData)(vlTOPp->io_b) 
                                                    >> 6U) 
                                                   & (IData)(vlTOPp->Adder__DOT___T_15_io_cout))) 
                                               | (((IData)(vlTOPp->io_a) 
                                                   >> 6U) 
                                                  & (IData)(vlTOPp->Adder__DOT___T_15_io_cout))));
    vlTOPp->io_cout = (1U & (((((IData)(vlTOPp->io_a) 
                                & (IData)(vlTOPp->io_b)) 
                               >> 7U) | (((IData)(vlTOPp->io_b) 
                                          >> 7U) & (IData)(vlTOPp->Adder__DOT___T_18_io_cout))) 
                             | (((IData)(vlTOPp->io_a) 
                                 >> 7U) & (IData)(vlTOPp->Adder__DOT___T_18_io_cout))));
    vlTOPp->io_sum = ((0x80U & ((0xffffff80U & ((IData)(vlTOPp->io_a) 
                                                ^ (IData)(vlTOPp->io_b))) 
                                ^ ((IData)(vlTOPp->Adder__DOT___T_18_io_cout) 
                                   << 7U))) | ((0x40U 
                                                & ((0xffffffc0U 
                                                    & ((IData)(vlTOPp->io_a) 
                                                       ^ (IData)(vlTOPp->io_b))) 
                                                   ^ 
                                                   ((IData)(vlTOPp->Adder__DOT___T_15_io_cout) 
                                                    << 6U))) 
                                               | ((0x20U 
                                                   & ((0xffffffe0U 
                                                       & ((IData)(vlTOPp->io_a) 
                                                          ^ (IData)(vlTOPp->io_b))) 
                                                      ^ 
                                                      ((IData)(vlTOPp->Adder__DOT___T_12_io_cout) 
                                                       << 5U))) 
                                                  | ((0x10U 
                                                      & ((0xfffffff0U 
                                                          & ((IData)(vlTOPp->io_a) 
                                                             ^ (IData)(vlTOPp->io_b))) 
                                                         ^ 
                                                         ((IData)(vlTOPp->Adder__DOT___T_9_io_cout) 
                                                          << 4U))) 
                                                     | ((8U 
                                                         & ((0xfffffff8U 
                                                             & ((IData)(vlTOPp->io_a) 
                                                                ^ (IData)(vlTOPp->io_b))) 
                                                            ^ 
                                                            ((IData)(vlTOPp->Adder__DOT___T_6_io_cout) 
                                                             << 3U))) 
                                                        | ((4U 
                                                            & ((0xfffffffcU 
                                                                & ((IData)(vlTOPp->io_a) 
                                                                   ^ (IData)(vlTOPp->io_b))) 
                                                               ^ 
                                                               ((IData)(vlTOPp->Adder__DOT___T_3_io_cout) 
                                                                << 2U))) 
                                                           | ((2U 
                                                               & ((0xfffffffeU 
                                                                   & ((IData)(vlTOPp->io_a) 
                                                                      ^ (IData)(vlTOPp->io_b))) 
                                                                  ^ 
                                                                  ((IData)(vlTOPp->Adder__DOT___T_io_cout) 
                                                                   << 1U))) 
                                                              | (1U 
                                                                 & (((IData)(vlTOPp->io_a) 
                                                                     ^ (IData)(vlTOPp->io_b)) 
                                                                    ^ (IData)(vlTOPp->io_cin))))))))));
}

void VAdder::_eval(VAdder__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VAdder::_eval\n"); );
    VAdder* __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    // Body
    vlTOPp->_combo__TOP__1(vlSymsp);
}

void VAdder::_eval_initial(VAdder__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VAdder::_eval_initial\n"); );
    VAdder* __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
}

void VAdder::final() {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VAdder::final\n"); );
    // Variables
    VAdder__Syms* __restrict vlSymsp = this->__VlSymsp;
    VAdder* __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
}

void VAdder::_eval_settle(VAdder__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VAdder::_eval_settle\n"); );
    VAdder* __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    // Body
    vlTOPp->_combo__TOP__1(vlSymsp);
}

VL_INLINE_OPT QData VAdder::_change_request(VAdder__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VAdder::_change_request\n"); );
    VAdder* __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    // Body
    // Change detection
    QData __req = false;  // Logically a bool
    return __req;
}

#ifdef VL_DEBUG
void VAdder::_eval_debug_assertions() {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VAdder::_eval_debug_assertions\n"); );
    // Body
    if (VL_UNLIKELY((clock & 0xfeU))) {
        Verilated::overWidthError("clock");}
    if (VL_UNLIKELY((reset & 0xfeU))) {
        Verilated::overWidthError("reset");}
    if (VL_UNLIKELY((io_cin & 0xfeU))) {
        Verilated::overWidthError("io_cin");}
}
#endif // VL_DEBUG

void VAdder::_ctor_var_reset() {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VAdder::_ctor_var_reset\n"); );
    // Body
    clock = VL_RAND_RESET_I(1);
    reset = VL_RAND_RESET_I(1);
    io_a = VL_RAND_RESET_I(8);
    io_b = VL_RAND_RESET_I(8);
    io_cin = VL_RAND_RESET_I(1);
    io_sum = VL_RAND_RESET_I(8);
    io_cout = VL_RAND_RESET_I(1);
    Adder__DOT___T_io_cout = VL_RAND_RESET_I(1);
    Adder__DOT___T_3_io_cout = VL_RAND_RESET_I(1);
    Adder__DOT___T_6_io_cout = VL_RAND_RESET_I(1);
    Adder__DOT___T_9_io_cout = VL_RAND_RESET_I(1);
    Adder__DOT___T_12_io_cout = VL_RAND_RESET_I(1);
    Adder__DOT___T_15_io_cout = VL_RAND_RESET_I(1);
    Adder__DOT___T_18_io_cout = VL_RAND_RESET_I(1);
    __Vm_traceActivity = VL_RAND_RESET_I(32);
}
