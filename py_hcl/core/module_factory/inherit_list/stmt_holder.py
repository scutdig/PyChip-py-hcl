from typing import Optional

from py_hcl.core.stmt import BlockStatement
from py_hcl.utils import auto_repr


@auto_repr
class StmtHolder(object):
    def __init__(self, module_name: str, top_statement: BlockStatement):
        self.module_name = module_name
        self.top_statement = top_statement


@auto_repr
class StmtNode(object):
    def __init__(self, stmt_holder: StmtHolder,
                 next_node: Optional["StmtNode"]):
        self.stmt_holder = stmt_holder
        self.next_node = next_node


@auto_repr
class StmtList(object):
    def __init__(self, stmt_list_head: StmtNode):
        self.stmt_list_head = stmt_list_head
