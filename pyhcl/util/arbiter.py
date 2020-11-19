from typing import List
from pyhcl import *


def Arbiter(gen, n):

    def log2Ceil(x):
        import math
        return math.ceil(math.log(x, 2))

    def scanLeft(l, v):
        def helper(f):
            s = v
            ret = [s]
            for item in l:
                s = f(s, item)
                ret.append(s)
            return ret
        return helper

    def ArbiterCtrl(request: List[bool]) -> List[bool]:
        if len(request) == 0:
            return []
        elif len(request) == 1:
            return [Bool(True)]
        else:
            return [Bool(True)] + list(map(lambda z: z == Bool(False),
                                           scanLeft(request[1:][:-1], request[0])(lambda x, y: x | y)))

    class clsArbiter(Module):
        io = IO(
            _in=Input(Vec(n, Decoupled(gen))),
            out=Output(Decoupled(gen)),
            chosen=Output(U.w(log2Ceil(n))),
        )
        io.chosen <<= U.w(log2Ceil(n))(n-1)
        io.out.bits <<= io._in[n-1].bits
        for i in range(n-2, -1, -1):
            with when(io._in[i].valid):
                io.chosen <<= U(i)
                io.out.bits <<= io._in[i].bits
        grant = ArbiterCtrl(list(map(lambda x: x.valid, io._in)))
        for _in, g in zip(io._in, grant):
            _in.ready <<= g & io.out.ready
        io.out.valid <<= (grant[-1] == Bool(False)) | io._in[n-1].valid

    return clsArbiter()

