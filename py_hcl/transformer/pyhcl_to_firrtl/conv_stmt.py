from multipledispatch import dispatch

from py_hcl.transformer.pyhcl_to_firrtl.conv_expr import convert_expr_by_id
from py_hcl.core.stmt import LineStatement, \
    ClusterStatement, ConditionStatement
from py_hcl.core.stmt.connect import Connect as HclConnect
from py_hcl.firrtl_ir.stmt.block import Block
from py_hcl.firrtl_ir.stmt.conditionally import Conditionally
from py_hcl.firrtl_ir.stmt.connect import Connect
from py_hcl.firrtl_ir.stmt.empty import EmptyStmt


@dispatch()
def convert_stmt(line: LineStatement):
    return convert_stmt(line.statement)


@dispatch()
def convert_stmt(cluster: ClusterStatement):
    return [ss for s in cluster.statements for ss in convert_stmt(s)]


@dispatch()
def convert_stmt(condition: ConditionStatement):
    cond_stmts, cond_ref = convert_expr_by_id(condition.seq_cond_id)
    seq = [ss for s in condition.seq_stmts for ss in convert_stmt(s)]
    alt = [EmptyStmt()] if condition.alt_stmts is None else \
        [ss for s in condition.alt_stmts for ss in convert_stmt(s)]

    conditionally = Conditionally(cond_ref, Block(seq), Block(alt))
    return [*cond_stmts, conditionally]


@dispatch()
def convert_stmt(connect: HclConnect):
    stmts_0, left_ref = convert_expr_by_id(connect.left_expr_id)
    stmts_1, right_ref = convert_expr_by_id(connect.right_expr_id)
    return [*stmts_0, *stmts_1, Connect(left_ref, right_ref)]
