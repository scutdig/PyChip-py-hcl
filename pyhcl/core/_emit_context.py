from collections import deque
from typing import Optional, Dict, Counter

from pyhcl.core._dynamic_ctx import DynamicContext
from pyhcl.ir import low_ir


class EmitterContext:
    def __init__(self, module: "Module",
                 emittedModules: Dict[int, low_ir.DefModule],
                 moduleNameCounter: Counter):

        # generate the name
        modClass = module.__class__
        self._modClass = modClass
        modName = modClass.__name__
        c = moduleNameCounter[modName]
        moduleNameCounter[modName] += 1
        self.name = modName + (("_" + str(c)) if c > 0 else "")

        # bunch of records
        self._module = module
        self._rawStatements = deque(modClass._statements)
        self._rawNameTable = modClass._rawTable
        self._emittedModules: Dict[int, low_ir.DefModule] = emittedModules
        self._moduleNameCounter = moduleNameCounter

        self._innerRef = {}

        self._finalStatements = {}
        self._finalPorts = []
        self._nameIndex = -1

    def prependRawStatement(self, statement):
        self._rawStatements.appendleft(statement)

    def appendFinalStatement(self, statement, scopeId):
        if self._finalStatements.get(scopeId) is None:
            self._finalStatements[scopeId] = []

        self._finalStatements[scopeId].append(statement)

    def getScopeStatements(self, scopeId):
        res = self._finalStatements[scopeId]
        return res

    def appendFinalPort(self, port):
        self._finalPorts.append(port)

    def updateRef(self, obj, ref):
        self._innerRef[id(obj)] = ref

    def getRef(self, obj) -> Optional:
        from pyhcl.core._meta_pub import Pub
        if isinstance(obj, Pub):
            obj = obj.value
        r = self._innerRef.get(id(obj))
        if r is not None:
            return r
        else:
            ref = obj.mapToIR(self)
            return ref

    def emit(self) -> Dict[int, low_ir.DefModule]:
        self._dealWithClockAndReset()
        scopeId = DynamicContext.currentScope()

        while len(self._rawStatements) > 0:
            lf = self._rawStatements.popleft()
            lf.mapToIR(self)

        modBundle = self._mapToBundle(self._finalPorts)
        finalMod = low_ir.Module(self.name,
                                 self._finalPorts,
                                 low_ir.Block(self.getScopeStatements(scopeId)),
                                 modBundle)

        self._emittedModules[id(self._modClass)] = finalMod

        return self._emittedModules

    def _dealWithClockAndReset(self):
        c = self._modClass.clock.public()
        r = self._modClass.reset.public()
        c.mapToIR(self)
        r.mapToIR(self)
        self._finalStatements[c.scopeId] = []

    def getName(self, obj):
        res = self._rawNameTable.get(id(obj))
        if res is not None:
            return res
        else:
            self._nameIndex += 1
            return "_T" + (("_" + str(self._nameIndex)) if self._nameIndex > 0 else "")

    def extendNewEnv(self, module):
        return EmitterContext(module, self._emittedModules, self._moduleNameCounter)

    def _mapToBundle(self, finalPorts):
        fs = []
        for i in finalPorts:
            if i.direction == low_ir.Input():
                fs.append(low_ir.Field(i.name, low_ir.Flip(), i.typ))
            else:
                fs.append(low_ir.Field(i.name, low_ir.Default(), i.typ))

        return low_ir.BundleType(fs)

    def getClock(self):
        return low_ir.Reference("clock", low_ir.ClockType())

    def getReset(self):
        return low_ir.Reference("reset", low_ir.UIntType(low_ir.IntWidth(1)))
