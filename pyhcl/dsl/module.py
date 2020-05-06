from pyhcl.core._dynamic_ctx import DynamicContext
from pyhcl.core._utils import get_attr
from pyhcl.core._repr import SubField
from pyhcl.dsl.cdatatype import Clock, U
from pyhcl.dsl.cio import Input, IO
from pyhcl.core._emit_context import EmitterContext
from pyhcl.ir import low_ir

shared_clock = Input(Clock())
shared_reset = Input(U.w(1))


class MetaModule(type):
    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)

        cls.clock = shared_clock
        cls.reset = shared_reset

        rawTable = {}
        for k, v in cls.__dict__.items():
            r = get_attr(v, 'extractForName')
            if r is not None:
                rawTable[id(r())] = k

        cls._rawTable = rawTable
        cls._statements = DynamicContext.get()


class Module(metaclass=MetaModule):
    def __init__(self):
        object.__setattr__(self, "scopeId", DynamicContext.currentScope())

    def __getattribute__(self, item: str):
        res = get_attr(self, item)
        res2 = get_attr(res, "public")
        if res2 is not None:
            return SubField(res2(), item, self)
        elif item == "mapToIR" or item.startswith("__"):
            return res
        else:
            return None

    def extractForName(self):
        return self

    def mapToIR(self, ctx: EmitterContext):
        name = ctx.getName(self)
        mod = self.__class__
        # ref = ctx._innerRef.get(id(mod))
        ref = ctx._innerRef.get(id(self))
        if ref is not None:
            return ref
        else:
            if id(mod) not in ctx._emittedModules:
                newEnv = ctx.extendNewEnv(self)
                newEnv.emit()

            mod = ctx._emittedModules[id(mod)]
            ref = low_ir.Reference(name, mod.typ)

            scopeId = get_attr(self, "scopeId")
            ctx.appendFinalStatement(low_ir.DefInstance(name, mod.name), scopeId)
            ctx.appendFinalStatement(low_ir.Connect(low_ir.SubField(ref, 'clock', low_ir.ClockType()),
                                                    ctx.getClock()), scopeId)
            ctx.appendFinalStatement(low_ir.Connect(low_ir.SubField(ref, 'reset', low_ir.UIntType(low_ir.IntWidth(1))),
                                                    ctx.getReset()), scopeId)
            ctx.updateRef(self, ref)

            return ref


class MetaBlackBox(type):
    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)

        stmts = DynamicContext.get()
        if len(stmts) != 0:
            raise Exception("BlackBox: included statements")

        io = []
        for k, v in cls.__dict__.items():
            if isinstance(v, IO):
                io.append(v)

        if len(io) > 1:
            raise Exception("BlackBox: too many IO objects")

        cls._ios = io


class BlackBox(metaclass=MetaBlackBox):
    def __init__(self):
        object.__setattr__(self, "scopeId", DynamicContext.currentScope())

    def __getattribute__(self, item: str):

        res = get_attr(self, item)
        res2 = get_attr(res, "public")
        if res2 is not None:
            r = res2()
            return Aux(r, self)
        elif item == "mapToIR" or item.startswith("__") or item.startswith("_"):
            return res
        else:
            return None

    def extractForName(self):
        return self

    def mapToIR(self, ctx: EmitterContext):
        insName = ctx.getName(self)
        mod = self.__class__
        ref = ctx._innerRef.get(id(self))
        if ref is not None:
            return ref
        else:
            if id(mod) not in ctx._emittedModules:
                self._emitExModule(mod, ctx)

            mod = ctx._emittedModules[id(mod)]
            ref = low_ir.Reference(insName, mod.typ)

            scopeId = get_attr(self, "scopeId")
            ctx.appendFinalStatement(low_ir.DefInstance(insName, mod.name), scopeId)
            ctx.updateRef(self, ref)

            return ref

    def _emitExModule(self, mod, ctx):
        # update module name count
        defname = mod.__name__
        c = ctx._moduleNameCounter[defname]
        ctx._moduleNameCounter[defname] += 1

        # construct module name
        name = defname + (("_" + str(c)) if c > 0 else "")

        # construct io field
        io = mod.io
        ports = []
        for k, v in io._ios.items():
            if isinstance(v, Input):
                d = low_ir.Input()
            else:
                d = low_ir.Output()
            ports.append(low_ir.Port(k, d, v.typ.mapToIR(ctx)))

        typ = self._mapToBundle(ports)
        m = low_ir.ExtModule(name, ports, defname, typ)

        ctx._emittedModules[id(mod)] = m

    def _mapToBundle(self, finalPorts):
        fs = []
        for i in finalPorts:
            if i.direction == low_ir.Input():
                fs.append(low_ir.Field(i.name, low_ir.Flip(), i.typ))
            else:
                fs.append(low_ir.Field(i.name, low_ir.Default(), i.typ))

        return low_ir.BundleType(fs)


class Aux:
    def __init__(self, io, top):
        self.io = io
        self.top = top

    def __getattribute__(self, item):
        io = get_attr(self, "io")
        r = io._ios[item]
        return SubField(r, item, get_attr(self, "top"))
