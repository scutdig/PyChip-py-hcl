from pyhcl.passes import check_form, check_types, check_widths, check_flows, auto_inferring
from pyhcl.ir.low_ir import *
class CheckAndInfer:
    @staticmethod
    def run(c: Circuit):
        c = check_form.CheckHighForm(c).run()
        c = auto_inferring.AutoInferring().run(c)
        c = check_types.CheckTypes().run(c)
        c = check_flows.CheckFlow().run(c)
        c = check_widths.CheckWidths().run(c)
        return c
        