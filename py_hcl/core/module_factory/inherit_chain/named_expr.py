from typing import Dict

from py_hcl.utils.serialization import json_serialize


@json_serialize
class NamedExprHolder(object):
    def __init__(self, module_name: str, named_expression_table: Dict[int,
                                                                      str]):
        self.module_name = module_name
        self.named_expression_table = named_expression_table
