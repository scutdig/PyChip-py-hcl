from typing import Optional

from py_hcl.core.stmt import ClusterStatement
from py_hcl.utils import json_serialize


@json_serialize
class StmtHolder(object):
    def __init__(self, module_name: str, top_statement: ClusterStatement):
        self.module_name = module_name
        self.top_statement = top_statement


@json_serialize
class StmtNode(object):
    def __init__(self, stmt_holder: StmtHolder,
                 next_node: Optional["StmtNode"]):
        self.stmt_holder = stmt_holder
        if next_node:
            self.next_node = next_node


@json_serialize
class StmtChain(object):
    def __init__(self, stmt_chain_head: StmtNode):
        self.stmt_chain_head = stmt_chain_head
