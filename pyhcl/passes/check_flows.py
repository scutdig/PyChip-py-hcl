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
            if isinstance(e, Reference):
                return flows[e.name]
            elif isinstance(e, SubIndex):
                return get_flow(e.expr, flows)
            elif isinstance(e, SubAccess):
                return get_flow(e.expr, flows)
            elif isinstance(e, SubField):
                if isinstance(e.expr.typ, BundleType):
                    for f in e.expr.typ.fields:
                        if f.name == e.name:
                            return times_g_flip(get_flow(e.expr, flows), f.flip)
            
            return SourceFlow()
            
        
        def flip_q(t: Type) -> bool:
            def flip_rec(t: Type, f: Orientation) -> bool:
                if isinstance(t, BundleType):
                    final = True
                    for field in t.fields:
                        final = flip_rec(field.typ, times_f_f(f, field.flip)) and final
                        return final
                elif isinstance(t, VectorType):
                    return flip_rec(t.typ, f)
                else:
                    return isinstance(f, Flip)
            return flip_rec(t, Default())
        
        def check_flow(info: Info, mname: str, flows: Dict[str, Flow], desired: Flow, e: Expression):
            flow = get_flow(e, flows)
            if isinstance(flow, SourceFlow) and isinstance(desired, SinkFlow):
                errors.append(WrongFlow(info, mname, e.serialize(), desired, flow))
            elif isinstance(flow, SinkFlow) and isinstance(desired, SourceFlow):
                # TODO: check PortKind or InstanceKind, but never implement.
                ...
            else:
                ...
        
        def check_flow_e(info: Info, mname: str, flows: Dict[str, Flow], e: Expression):
            if isinstance(e, Mux):
                for _, ee in e.__dict__.items():
                    if isinstance(ee, Expression):
                        check_flow(info, mname, flows, SourceFlow(), ee)
            if isinstance(e, DoPrim):
                for ee in e.args:
                    if isinstance(ee, Expression):
                        check_flow(info, mname, flows, SourceFlow(), ee)
            
            for _, ee in e.__dict__.items():
                    if isinstance(ee, Expression):
                        check_flow_e(info, mname, flows, ee)
        
        def check_flow_s(minfo: Info, mname: str, flows: Dict[str, Flow], s: Statement):
            info = lambda s: minfo if isinstance(s, NoInfo) else s.info
            if isinstance(s, DefWire):
                flows[s.name] = DuplexFlow()
            elif isinstance(s, DefRegister):
                flows[s.name] = DuplexFlow()
            elif isinstance(s, DefMemory):
                flows[s.name] = SourceFlow()
            elif isinstance(s, DefInstance):
                flows[s.name] = SourceFlow()
            elif isinstance(s, DefNode):
                check_flow(info, mname, flows, SourceFlow(), s.value)
                flows[s.name] = SourceFlow()
            elif isinstance(s, DefMemPort):
                flows[s.name] = SinkFlow()
            elif isinstance(s, Connect):
                check_flow(info, mname, flows, SinkFlow(), s.loc)
                check_flow(info, mname, flows, SourceFlow(), s.expr)
                ...
            elif isinstance(s, Conditionally):
                check_flow(info, mname, flows, SourceFlow(), s.pred)
            else:
                ...
            
            for _, ss in s.__dict__.items():
                if isinstance(ss, Expression):
                    check_flow_e(info, mname, flows, ss)
                if isinstance(ss, Statement):
                    check_flow_s(minfo, mname, flows, ss)
        
        for m in c.modules:
            flows: Dict[str, Flow] = {}
            if hasattr(m, 'ports') and isinstance(m.ports, list):
                for p in m.ports:
                    flows[p.name] = to_flow(p.direction)
        
            if hasattr(m, 'body') and isinstance(m.body, Block):
                if hasattr(m.body, 'stmts') and isinstance(m.body.stmts, list):
                    for stmt in m.body.stmts:
                        check_flow_s(m.info, m.name, flows, stmt)
        
        errors.trigger()
        return c
