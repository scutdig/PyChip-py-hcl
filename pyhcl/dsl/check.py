from pyhcl.passes import check_form, check_types, check_widths, check_flows, infer_types, infer_widths
from pyhcl.ir.low_ir import *
class CheckUtils:
    @staticmethod
    def run_check(c: Circuit):
        c = check_form.CheckHighForm(c).run()
        c = check_types.CheckTypes().run(c)
        c = check_flows.CheckFlow().run(c)
        c = check_widths.CheckWidths().run(c)
        c = infer_types.InferTypes().run(c)
        c = infer_widths.InferWidths().run(c)
        return c
        