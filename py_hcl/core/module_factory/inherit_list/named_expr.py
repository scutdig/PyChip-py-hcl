from typing import Optional, Dict

from py_hcl.utils import json_serialize


@json_serialize
class NamedExprHolder(object):
    def __init__(self, module_name: str,
                 named_expression_table: Dict[int, str]):
        self.module_name = module_name
        self.named_expression_table = named_expression_table


@json_serialize
class NamedExprNode(object):
    def __init__(self,
                 named_expr_holder: NamedExprHolder,
                 next_node: Optional["NamedExprNode"]):
        self.named_expr_holder = named_expr_holder
        if next_node:
            self.next_node = next_node


@json_serialize
class NamedExprChain(object):
    def __init__(self, named_expr_chain_head: NamedExprNode):
        self.named_expr_chain_head = named_expr_chain_head
