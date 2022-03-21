from pyhcl.passes import check_form, check_types, check_widths, check_flows
from pyhcl.ir.low_ir import *
class CheckUtils:
    @staticmethod
    def run_check(c: Circuit):
        c = check_form.CheckHighForm(c).run()
        c = check_types.CheckTypes().run(c)
        c = check_flows.CheckFlow().run(c)
        return c
        