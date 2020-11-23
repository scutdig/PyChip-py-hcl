from py_hcl.core.stmt import ClusterStatement
from py_hcl.utils.serialization import json_serialize


@json_serialize
class StmtHolder(object):
    def __init__(self, module_name: str, top_statement: ClusterStatement):
        self.module_name = module_name
        self.top_statement = top_statement
