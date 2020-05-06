// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table internal header
//
// Internal details; most calling programs do not need this header,
// unless using verilator public meta comments.

#ifndef _VAdder__Syms_H_
#define _VAdder__Syms_H_

#include "verilated.h"

// INCLUDE MODULE CLASSES
#include "VAdder.h"

// SYMS CLASS
class VAdder__Syms : public VerilatedSyms {
  public:
    
    // LOCAL STATE
    const char* __Vm_namep;
    bool __Vm_activity;  ///< Used by trace routines to determine change occurred
    bool __Vm_didInit;
    
    // SUBCELL STATE
    VAdder*                        TOPp;
    
    // CREATORS
    VAdder__Syms(VAdder* topp, const char* namep);
    ~VAdder__Syms() {}
    
    // METHODS
    inline const char* name() { return __Vm_namep; }
    inline bool getClearActivity() { bool r=__Vm_activity; __Vm_activity=false; return r; }
    
} VL_ATTR_ALIGNED(64);

#endif  // guard
