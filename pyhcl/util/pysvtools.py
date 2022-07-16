import dataclasses
import os
import warnings
from os import abort

from pyhcl.dsl.module import MetaBlackBox
from pyhcl.dsl.cio import Input, Output
from pyhcl.dsl.cdatatype import *
from pysv import DataType, sv, compile_lib, generate_sv_binding

from pyhcl.util.functions import make_dirs


class PysvModGen:
    def __init__(self, name: str, inputs: {}, outputs: {}, funcname):
        self.name = name
        self.inputs = inputs
        self.outputs = outputs

        self.fname = funcname
        self.name_wid_map = {}


    # map to wire or reg 's name
    def nm(self, name):
        return "__tmp_"+name


    def input_ports(self):
        str = ""
        for k, v in self.inputs.items():
            _, w = self.typeinfo(v)
            w = int(w)
            wstr=""
            if w != 1:
                wstr = f"[{w-1}:0]"
            self.name_wid_map[k] = wstr
            str += f"\tinput {wstr}\t\t{k} ,\n"
        return str

    def output_ports(self):
        str = ""
        for k, v in self.outputs.items():
            _, w = self.typeinfo(v)
            w = int(w)
            wstr=""
            if w != 1:
                wstr = f"[{w-1}:0]"
            self.name_wid_map[k] = wstr
            str += f"\toutput {wstr}\t\t{k} ,\n"
        return str

    def def_wires(self):
        res = ""
        for k in self.inputs.keys():
            res += f"\twire {self.name_wid_map[k]}\t{self.nm(k)} ;\n"
        return res

    def def_regs(self):
        res = ""
        for k in self.outputs.keys():
            res += f"\treg {self.name_wid_map[k]}\t{self.nm(k)} ;\n"
        return res

    def assign_wires(self):
        res = ""
        for k in self.inputs.keys():
            res += f"\tassign {self.nm(k)} = {k} ;\n"
        return res

    def assign_regs(self):
        res = ""
        for k in self.outputs.keys():
            res += f"\tassign {k} = {self.nm(k)} ;\n"
        return res

    def modname(self):
        return self.name

    def funcname(self):
        return self.fname

    def funcargs(self):
        str = ""
        if len(self.inputs) == 0:
            return str
        for k in self.inputs.keys():
            str += f"{self.nm(k)}, "
        if len(self.outputs) == 0:
            return str
        for k in self.outputs.keys():
            str += f"{self.nm(k)}, "
        return str[:-2]

    # return type must be written as Reference
    # so this function will not be called
    def retvalues(self):
        str = ""
        if len(self.outputs) == 0:
            return str
        # return type must be written as Reference
        for k in self.outputs.keys():
            str += f"{k}, "
        return str[:-2]

    """demo 
    // Pysv
    module Xor(
        input 		in1 ,
        input 		in2 ,
    
        output 		out 
        );
        wire 	__tmp_in1 ;
        wire 	__tmp_in2 ;
    
        reg 	__tmp_out ;
    
        assign __tmp_in1 = in1 ;
        assign __tmp_in2 = in2 ;
    
    
        import pysv::* ;
        initial begin
            fn(__tmp_in1, __tmp_in2, __tmp_out)
        end
        assign out = __tmp_out ;
    
    endmodule
    """
    def tosvmodule(self):
        res = "// Pysv\n"
        res += f"module {self.modname()}(\n"
        res += f"{self.input_ports()}\n{self.output_ports()}\n"
        res = res[:-3] + "\n\t);\n"

        res += f"{self.def_wires()}\n{self.def_regs()}\n"
        res += f"{self.assign_wires()}\n\n"

        res += f"\timport pysv::* ;\n"
        #res += f"\tinitial begin\n"
        res += f"\talways begin\n"
        res += f"\t\t{self.funcname()}({self.funcargs()}) ;\n"
        res += f"\tend\n"

        res += f"{self.assign_regs()}\n"
        res += f"endmodule\n"
        return res

    def typeinfo(self, typ):
        typestr = str(typ)
        f = typestr.rfind(".")
        b = typestr.rfind("\\")
        typ = typestr[f+1]
        width = typestr[f+2:b-1]
        return typ, width

    # not support String and Object  yet
    def typmapper(self, typ):
        if isinstance(typ, Clock):
            return DataType.Bit

        us, wid = self.typeinfo(typ)
        finalstr = us+wid

        map = {
            "U1" : DataType.Bit,
            "U4" : DataType.UByte,
            "U8" : DataType.UShortInt,
            "U32" : DataType.UInt,
            "U64" : DataType.ULongInt,
            "S1": DataType.Bit,
            "S4" : DataType.Byte,
            "S8" : DataType.ShortInt,
            "S32" : DataType.Int,
            "S64" : DataType.LongInt,
        }

        if int(wid) not in [1, 4, 8, 32, 64]:
            warnings.warn("No matched type, width must be 1, 4, 8, 32, 64")
            abort()
        return map[finalstr]




def filterIOs(bbox):
    inputs = {}
    outputs = {}
    ios = bbox.io.value._ios
    for k, v in ios.items():
        if type(v) == Input:
            inputs[k] = v.typ
        else:
            outputs[k] = v.typ
    return inputs, outputs

bboxs_list = {}


def addpysvmodule(bbox: MetaBlackBox, func, path=".sv/bbox"):
    # need some check on bbox ios and func args
    if bbox in bboxs_list:
        warnings.warn("One BBOX can only have one function")
        abort()
    inputs, outputs = filterIOs(bbox)
    name = bbox.__name__
    modgen = PysvModGen(name, inputs, outputs, func.func_name)
    sv = modgen.tosvmodule()
    filepath = f"{path}/{name}.sv"
    make_dirs(filepath)
    with open(filepath, "w") as f:
        f.write(sv)
    bboxs_list[bbox] = func


def compile_and_binding_all():
    print("\n\n-----------------------pysv build info---------------------------\n")
    funclist = bboxs_list.values()
    # compile the a shared_lib into build folder
    lib_path = compile_lib(funclist, cwd=".build")
    # generate SV binding
    generate_sv_binding(funclist, filename=".sv/pkg/pysv_pkg.sv")


def compile_and_binding_all_func(funclist):
    print("\n\n-----------------------pysv build info---------------------------\n")
    # funclist = bboxs_list.values()
    # compile the a shared_lib into build folder
    lib_path = compile_lib(funclist, cwd=".build")
    # generate SV binding
    generate_sv_binding(funclist, filename=".sv/pkg/pysv_pkg.sv")