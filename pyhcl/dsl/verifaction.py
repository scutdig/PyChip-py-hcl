from pyhcl.ir import low_ir
from pyhcl.core._dynamic_ctx import DynamicContext

class _Verfication:
    def __init__(self, clk, pred, en, msg=""):
        self.clk = clk
        self.pred = pred
        self.en = en
        self.msg = msg
        self.scopeId = DynamicContext.currentScope()


class doAssert(_Verfication):
    def __init__(self, clk, pred, en, msg):
        super().__init__(clk, pred, en, msg)

    def mapToIR(self, ctx):
        ref_clk = ctx.getRef(self.clk)
        ref_pred = ctx.getRef(self.pred)
        ref_en = ctx.getRef(self.en)
        res = low_ir.Assert(ref_clk, ref_pred, ref_en, self.msg)
        ctx.appendFinalStatement(res, self.scopeId)
        return res

class doAssume(_Verfication):
    def __init__(self, clk, pred, en, msg=""):
        super().__init__(clk, pred, en, msg)

    def mapToIR(self, ctx):
        ref_clk = ctx.getRef(self.clk)
        ref_pred = ctx.getRef(self.pred)
        ref_en = ctx.getRef(self.en)
        res = low_ir.Assume(ref_clk, ref_pred, ref_en, self.msg)
        ctx.appendFinalStatement(res, self.scopeId)
        return res

class doCover(_Verfication):
    def __init__(self, clk, pred, en, msg=""):
        super().__init__(clk, pred, en, msg)
        self.scopeId = DynamicContext.currentScope()

    def mapToIR(self, ctx):
        ref_clk = ctx.getRef(self.clk)
        ref_pred = ctx.getRef(self.pred)
        ref_en = ctx.getRef(self.en)
        res = low_ir.Cover(ref_clk, ref_pred, ref_en, self.msg)
        ctx.appendFinalStatement(res, self.scopeId)
        return res

