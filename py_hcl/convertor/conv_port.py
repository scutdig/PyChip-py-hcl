from typing import Dict, Union, List

from py_hcl.convertor.conv_type import convert_type
from py_hcl.core.expr.io import Input, Output
from py_hcl.firrtl_ir.stmt.defn.module import InputPort, OutputPort
from py_hcl.firrtl_ir.type import ClockType, UIntType, BundleType
from py_hcl.firrtl_ir.type.field import Field
from py_hcl.firrtl_ir.type.width import Width


def convert_ports(raw_ports: Dict[str, Union[Input, Output]]):
    ports = [InputPort('clock', ClockType()),
             InputPort('reset', UIntType(Width(1)))]
    for k, v in raw_ports.items():
        p = InputPort if v.port_dir == 'input' else OutputPort
        ports.append(p(k, convert_type(v.hcl_type)))
    return ports


def ports_to_bundle_type(ports: List[Union[InputPort, OutputPort]]):
    fields = []
    for p in ports:
        if isinstance(p, InputPort):
            fields.append(Field(p.name, p.tpe, True))
        else:
            fields.append(Field(p.name, p.tpe, False))
    return BundleType(fields)
