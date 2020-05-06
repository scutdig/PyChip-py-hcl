from __future__ import annotations

from pyhcl.core._cond import CondBlock, When, Elsewhen, Otherwise
from pyhcl.core._dynamic_ctx import DynamicContext


class when:
    def __init__(self, condition):
        self.__cond = condition
        self.cb = CondBlock()

    def __enter__(self):
        DynamicContext.push(self)
        self.ownScope = DynamicContext.createScope()

    def __exit__(self, exc_type, exc_val, exc_tb):
        result = []
        top = DynamicContext.pop()
        while id(top) != id(self):
            result.append(top)
            top = DynamicContext.pop()
        result.reverse()

        a = When(self.__cond, result)
        a.ownScope = self.ownScope

        self.cb.when = a
        DynamicContext.push(self.cb)
        DynamicContext.deleteScope()


class elsewhen:
    def __init__(self, condition):
        self.__cond = condition

    def __enter__(self):
        DynamicContext.push(self)
        self.ownScope = DynamicContext.createScope()

    def __exit__(self, exc_type, exc_val, exc_tb):
        result = []
        top = DynamicContext.pop()
        while id(top) != id(self):
            result.append(top)
            top = DynamicContext.pop()
        result.reverse()
        a = Elsewhen(self.__cond, result)
        a.ownScope = self.ownScope

        p = DynamicContext.pop()
        if not isinstance(p, CondBlock) or not p.canAcceptElsewhen():
            raise Exception("syntax error")
        else:
            DynamicContext.push(p.withElsewhen(a))
            DynamicContext.deleteScope()


class otherwise:
    def __enter__(self):
        DynamicContext.push(self)
        self.ownScope = DynamicContext.createScope()

    def __exit__(self, exc_type, exc_val, exc_tb):
        result = []
        top = DynamicContext.pop()
        while id(top) != id(self):
            result.append(top)
            top = DynamicContext.pop()
        result.reverse()

        a = Otherwise(result)
        a.ownScope = self.ownScope

        p = DynamicContext.pop()

        if not isinstance(p, CondBlock) or not p.canAcceptOtherwise():
            raise Exception("syntax error")
        else:
            DynamicContext.push(p.withOtherwise(a))
            DynamicContext.deleteScope()


