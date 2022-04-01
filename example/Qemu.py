from pyhcl import *
from pprint import pprint
from time import time

if __name__ == '__main__':
    q = Qemu("rv64", "/tmp/favourite_architecture/share/main")
    t1 = time()
    for i in range(100):
        regs = q.step()
    pprint(regs)
    t2 = time()
    print("t2 - t1 " + str(t2 - t1))