# from pyhcl import *
# from example import half_adder
# from example import simlite
# from example import simlite_2
# from example import Simlite_task
# from injector import simlite_v3

# from injector import simlite_v2
# from injector import simlite_v4

# from myTests import test_simlite
# from myTests import test_simlite_pysv
# from myTests import test_simlite_fork

from myTests import test_verilog
# from myTests import test_verilog_pysv
from myTests import test_verilog_fork

# from myTests import test_firrtl
# from myTests import test_firrtl_2


# class MOD(Module):
#     io = IO(
#         a=Input(U.w(32)),
#         b=Input(U.w(32)),
#         e=Input(Bool),
#         z=Output(U.w(32)),
#     )
#
#     x = RegInit(U.w(32)(0))
#     y = RegInit(U.w(32)(0))
#
#     with when(x >= y):
#         x <<= x - y
#
#     with when(io.e):
#         x <<= io.a
#         y <<= io.b
#
#     io.z <<= x


def main():
    # f = Emitter.dump(Emitter.emit(MOD()), "mod.v")
    # Emitter.dumpVerilog(f)
    # half_adder.main()

    # simlite_v2.main()
    # simlite_v4.main()


    # simlite_2.main()
    # Simlite_task.test()

    # test_simlite.main()
    # test_simlite_pysv.main()
    # test_simlite_fork.main()

    test_verilog.main()
    # test_verilog_pysv.main()
    # test_verilog_fork.main()

    # test_firrtl.main()
    # test_firrtl_2.main()
    pass


if __name__ == '__main__':
    main()


