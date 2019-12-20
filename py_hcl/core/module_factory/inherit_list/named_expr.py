from typing import Optional, Dict

from py_hcl.core.expr import HclExpr
from py_hcl.utils import auto_repr


@auto_repr
class NamedExprHolder(object):
    def __init__(self, module_name: str,
                 named_expressions: Dict[str, HclExpr]):
        self.module_name = module_name
        self.named_expressions = named_expressions


@auto_repr
class NamedExprNode(object):
    def __init__(self,
                 named_expr_holder: NamedExprHolder,
                 next_node: Optional["NamedExprNode"]):
        self.named_expr_holder = named_expr_holder
        self.next_node = next_node


@auto_repr
class NamedExprList(object):
    def __init__(self, named_expr_list_head: NamedExprNode):
        self.named_expr_list_head = named_expr_list_head
