import random
import uuid

from py_hcl.firrtl_ir.shortcuts import w, uw, u, s, sw, n, vec
from py_hcl.firrtl_ir.type import UIntType, SIntType, \
    UnknownType, BundleType, VectorType, ClockType
from py_hcl.firrtl_ir.type.field import Field
from py_hcl.firrtl_ir.type_checker import check
from py_hcl.utils import signed_num_bin_len, unsigned_num_bin_len


class OpCase(object):
    def __init__(self, op):
        self.op = op
        self.args = []
        self.const_args = []
        self.res_type_fn = None
        self.valid_filter = lambda *_: True

    def arg_types(self, *arg_types):
        self.args = arg_types
        return self

    def const_arg_types(self, *const_arg_types):
        self.const_args = const_arg_types
        return self

    def res_type(self, res_type_fn):
        self.res_type_fn = res_type_fn
        return self

    def filter(self, valid_fn):
        self.valid_filter = valid_fn
        return self


def int_gen():
    return random.randint(0, 20)


def name_gen():
    return "n" + str(uuid.uuid4()).replace("-", "")


def u_gen():
    if random.randint(0, 1):
        rand_u_value = random.randint(0, 1024)
        rand_u_value_width = unsigned_num_bin_len(rand_u_value)
        rand_u_width = random.randint(rand_u_value_width,
                                      2 * rand_u_value_width)
        return u(rand_u_value, w(rand_u_width))
    else:
        rand_nu_name = name_gen()
        rand_nu_width = random.randint(1, 20)
        return n(rand_nu_name, uw(rand_nu_width))


def s_gen():
    if random.randint(0, 1):
        rand_s_value = random.randint(-1024, 1024)
        rand_s_value_width = signed_num_bin_len(rand_s_value)
        rand_s_width = random.randint(rand_s_value_width,
                                      2 * rand_s_value_width)
        return s(rand_s_value, w(rand_s_width))
    else:
        rand_ns_name = name_gen()
        rand_ns_width = random.randint(1, 20)
        return n(rand_ns_name, sw(rand_ns_width))


def uw_gen():
    rand_width = random.randint(1, 20)
    return uw(rand_width)


def sw_gen():
    rand_width = random.randint(1, 20)
    return sw(rand_width)


def unknown_gen():
    return n(name_gen(), UnknownType())


def clock_gen():
    return n(name_gen(), ClockType())


def vec_gen():
    rand_num = random.randint(1, 100)
    seed = random.choices(population=[1, 2, 3, 4],
                          weights=[0.4, 0.4, 0.1, 0.1],
                          k=1)[0]
    if seed == 1:
        return vec(uw_gen(), rand_num)
    elif seed == 2:
        return vec(sw_gen(), rand_num)
    elif seed == 3:
        return vec(vec_gen(), rand_num)
    elif seed == 4:
        return vec(bdl_gen(), rand_num)


def bdl_gen():
    rand_num = random.randint(1, 5)
    fields = []
    for i in range(rand_num):
        rand_name = name_gen()
        rand_bool = random.choice([True, False])
        seed = random.choices(population=[1, 2, 3, 4],
                              weights=[0.4, 0.4, 0.1, 0.1],
                              k=1)[0]
        if seed == 1:
            fields.append(Field(rand_name, uw_gen(), rand_bool))
        elif seed == 2:
            fields.append(Field(rand_name, sw_gen(), rand_bool))
        elif seed == 3:
            fields.append(Field(rand_name, vec_gen(), rand_bool))
        elif seed == 4:
            fields.append(Field(rand_name, bdl_gen(), rand_bool))
    return BundleType(fields)


obj_gen_map = {
    UIntType: u_gen,
    SIntType: s_gen,
    UnknownType: unknown_gen,
    ClockType: clock_gen,
    VectorType: vec_gen,
    BundleType: bdl_gen,
    int: int_gen,
}


def obj_gen(case):
    while True:
        args = [obj_gen_map[a]() for a in case.args]
        const_args = [obj_gen_map[a]() for a in case.const_args]

        construct_args = []
        if len(args) > 1:
            construct_args.append(args)
        elif len(args) == 1:
            construct_args.append(args[0])

        if len(const_args) > 1:
            construct_args.append(const_args)
        elif len(const_args) == 1:
            construct_args.append(const_args[0])

        if case.valid_filter(*args, *const_args):
            break

    construct_args.append(case.res_type_fn(*args, *const_args))

    return case.op(*construct_args)


def basis_tester(cases):
    for case in cases:
        for i in range(5):
            obj = obj_gen(case)
            assert check(obj)


def encounter_error_tester(cases):
    for case in cases:
        for i in range(5):
            obj = obj_gen(case)
            assert not check(obj)


def op_args(op, *arg_types):
    class C:
        @staticmethod
        def tpe(res_type):
            return OpCase(op).arg_types(*arg_types).res_type(res_type)

    return C


def type_wrong_cases_2_args_gen(op):
    wrong_cases = [
        op_args(op, UnknownType, UnknownType).tpe(lambda x, y: uw(32)),
        op_args(op, UnknownType, UIntType).tpe(lambda x, y: uw(32)),
        op_args(op, UnknownType, SIntType).tpe(lambda x, y: sw(32)),
        op_args(op, UnknownType, VectorType).tpe(lambda x, y: sw(32)),
        op_args(op, UnknownType, BundleType).tpe(lambda x, y: sw(32)),
        op_args(op, UIntType, VectorType).tpe(lambda x, y: uw(32)),
        op_args(op, UIntType, BundleType).tpe(lambda x, y: uw(32)),
        op_args(op, UIntType, UnknownType).tpe(lambda x, y: uw(32)),
        op_args(op, SIntType, VectorType).tpe(lambda x, y: sw(32)),
        op_args(op, SIntType, BundleType).tpe(lambda x, y: sw(32)),
        op_args(op, SIntType, UnknownType).tpe(lambda x, y: sw(32)),
        op_args(op, VectorType, UIntType).tpe(lambda x, y: uw(32)),
        op_args(op, VectorType, SIntType).tpe(lambda x, y: sw(32)),
        op_args(op, VectorType, VectorType).tpe(lambda x, y: uw(32)),
        op_args(op, VectorType, BundleType).tpe(lambda x, y: uw(32)),
        op_args(op, BundleType, UIntType).tpe(lambda x, y: uw(32)),
        op_args(op, BundleType, SIntType).tpe(lambda x, y: uw(32)),
        op_args(op, BundleType, VectorType).tpe(lambda x, y: uw(32)),
        op_args(op, BundleType, UnknownType).tpe(lambda x, y: uw(32)),
        op_args(op, BundleType, BundleType).tpe(lambda x, y: uw(32)),
    ]
    return wrong_cases


def type_wrong_cases_1_arg_gen(op):
    wrong_cases = [
        op_args(op, UnknownType).tpe(lambda x: uw(32)),
        op_args(op, VectorType).tpe(lambda x: uw(32)),
        op_args(op, BundleType).tpe(lambda x: uw(32)),
    ]
    return wrong_cases


def width(x):
    return x.tpe.width.width


def max_width(x, y):
    return max(width(x), width(y))


def min_width(x, y):
    return min(width(x), width(y))


def sum_width(x, y):
    return width(x) + width(y)
