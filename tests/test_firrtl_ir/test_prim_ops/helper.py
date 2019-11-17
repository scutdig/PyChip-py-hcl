import random
import uuid

from py_hcl.firrtl_ir.shortcuts import w, uw, u, s, sw, n, vec
from py_hcl.firrtl_ir.type import UIntType, SIntType, \
    UnknownType, BundleType, VectorType
from py_hcl.firrtl_ir.type.field import Field
from py_hcl.firrtl_ir.type_checker import check, OpTypeChecker
from py_hcl.firrtl_ir.utils import unsigned_num_bin_len, signed_num_bin_len


class OpCase(object):
    def __init__(self, op):
        self.op = op
        self.args = None
        self.res_type_fn = None

    def arg_types(self, *arg_types):
        self.args = arg_types
        return self

    def res_type(self, res_type_fn):
        self.res_type_fn = res_type_fn
        return self


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
    return UnknownType()


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
    VectorType: vec_gen,
    BundleType: bdl_gen
}


def obj_gen(case):
    args = [obj_gen_map[a]() for a in case.args]
    res_type = case.res_type_fn(*args)
    return case.op(args, res_type)


def basis_tester(cases):
    for case in cases:
        for i in range(5):
            obj = obj_gen(case)
            assert OpTypeChecker.check(obj)
            assert check(obj)


def encounter_error_tester(cases):
    for case in cases:
        for i in range(5):
            obj = obj_gen(case)
            assert not OpTypeChecker.check(obj)
            assert not check(obj)


if __name__ == '__main__':
    from io import BytesIO

    output = BytesIO()
    vec_gen().serialize(output)
    output.flush()

    print(str(output.getvalue(), "utf-8"))
