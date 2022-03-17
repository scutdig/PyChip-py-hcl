from typing import List
from pyhcl.ir.low_ir import *
from pyhcl.ir.low_prim import *
from pyhcl.passes._pass import Pass, PassException, Error
from pyhcl.passes.utils import times_f_f, times_g_flip, to_flow
from pyhcl.passes.wir import *

class WrongFlow(PassException):
    def __init__(self, info: Info, mname: str, expr: str, wrong: Flow, right: Flow):
        super().__init__(f'{info}: [module {mname}] Expression {expr} is used as a {wrong} but can only be used as a {right}.')

class CheckFlow(Pass):
    def run(self, c: Circuit):
        errors = Error()

        def get_flow(e: Expression, flows: Dict[str, Flow]) -> Flow:
            if type(e) == Reference:
                return flows[e.name]
            elif type(e) == SubIndex:
                return get_flow(e.expr, flows)
            elif type(e) == SubAccess:
                return get_flow(e.expr, flows)
            elif type(e) == SubField:
                if type(e.expr.typ) == BundleType:
                    for f in e.expr.typ.fields:
                        if f.name == e.name:
                            return times_g_flip(get_flow(e.expr, flows), f.flip)
            
            return SourceFlow()
            
        
        def flip_q(t: Type) -> bool:
            def flip_rec(t: Type, f: Orientation) -> bool:
                if type(t) == BundleType:
                    final = True
                    for field in t.fields:
                        final = flip_rec(field.typ, times_f_f(f, field.flip)) and final
                        return final
                elif type(t) == VectorType:
                    return flip_rec(t.typ, f)
                else:
                    return type(f) == Flip
            return flip_rec(t, Default())
        
        def check_flow(info: Info, mname: str, flows: Dict[str, Flow], desired: Flow, e: Expression):
            flow = get_flow(e, flows)
            if type(flow) == SourceFlow and type(desired) == SinkFlow:
                errors.append(WrongFlow(info, mname, e.serialize(), desired, flow))
            elif type(flow) == SinkFlow and type(desired) == SourceFlow:
                # TODO check PortKind or InstanceKind
                ...
            else:
                ...
        
        def check_flow_e(info: Info, mname: str, flows: Dict[str, Flow], e: Expression):
            if type(e) == Mux:
                for _, ee in e.__dict__.items():
                    if type(ee) == Expression:
                        check_flow(info, mname, flows, SourceFlow(), ee)
            if type(e) == DoPrim:
                for _, ee in e.args.__dict__.items():
                    if type(ee) == Expression:
                        check_flow(info, mname, flows, SourceFlow(), ee)
            
            for _, ee in e.__dict__.items():
                    if type(ee) == Expression:
                        check_flow_e(info, mname, flows, SourceFlow(), ee)
        
        def check_flow_s(minfo: Info, mname: str, flows: Dict[str, Flow], s: Statement):
            info = lambda s: minfo if type(s) == NoInfo else s
            if type(s) == DefWire:
                flows[s.name] = DuplexFlow()
            elif type(s) == DefRegister:
                flows[s.name] = DuplexFlow()
            elif type(s) == DefMemory:
                flows[s.name] == SourceFlow()
            elif type(s) == DefInstance:
                flows[s.name] == SourceFlow()
            elif type(s) == DefNode:
                check_flow(info, mname, flows, SourceFlow(), s)
                flows[s.name] = SourceFlow()
            elif type(s) == Connect:
                check_flow(info, mname, flows, SinkFlow(), s.loc)
                check_flow(info, mname, flows, SourceFlow(), s.expr)
            elif type(s) == Conditionally:
                check_flow(info, mname, flows, SourceFlow(), s.pred)
            else:
                ...
            
            for _, ss in s.__dict__.items():
                if type(ss) == Expression:
                    check_flow_e(info, mname, flows)
                if type(ss) == Statement:
                    check_flow_s(minfo, mname, flows)
        
        for m in c.modules:
            flows: Dict[str, Flow] = {}
            for p in m.ports:
                flows[p.name] = to_flow(p.direction)
            for stmt in m.body.stmts:
                check_flow_s(m.info, m.name, flows, stmt)
        
        errors.trigger()
        return c
