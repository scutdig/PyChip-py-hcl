import logging
import socket
from time import sleep, time
import os
from pprint import pprint


def swab32(data):
    res = ""
    for i in range(4):
        res = data[i * 2:i * 2 + 2] + res
    return res

def swab64(data):
    res = ""
    for i in range(8):
        res = data[i * 2:i * 2 + 2] + res
    return res


"""
RISV64 SUPPORT
"""

rv64_regs = [
    {"reg_name": "zero", "bitsize": 64, "type": "int"},
    {"reg_name": "ra", "bitsize": 64, "type": "code_ptr"},
    {"reg_name": "sp", "bitsize": 64, "type": "data_ptr"},
    {"reg_name": "gp", "bitsize": 64, "type": "data_ptr"},
    {"reg_name": "tp", "bitsize": 64, "type": "data_ptr"},
    {"reg_name": "t0", "bitsize": 64, "type": "int"},
    {"reg_name": "t1", "bitsize": 64, "type": "int"},
    {"reg_name": "t2", "bitsize": 64, "type": "int"},
    {"reg_name": "fp", "bitsize": 64, "type": "data_ptr"},
    {"reg_name": "s1", "bitsize": 64, "type": "int"},
    {"reg_name": "a0", "bitsize": 64, "type": "int"},
    {"reg_name": "a1", "bitsize": 64, "type": "int"},
    {"reg_name": "a2", "bitsize": 64, "type": "int"},
    {"reg_name": "a3", "bitsize": 64, "type": "int"},
    {"reg_name": "a4", "bitsize": 64, "type": "int"},
    {"reg_name": "a5", "bitsize": 64, "type": "int"},
    {"reg_name": "a6", "bitsize": 64, "type": "int"},
    {"reg_name": "a7", "bitsize": 64, "type": "int"},
    {"reg_name": "s2", "bitsize": 64, "type": "int"},
    {"reg_name": "s3", "bitsize": 64, "type": "int"},
    {"reg_name": "s4", "bitsize": 64, "type": "int"},
    {"reg_name": "s5", "bitsize": 64, "type": "int"},
    {"reg_name": "s6", "bitsize": 64, "type": "int"},
    {"reg_name": "s7", "bitsize": 64, "type": "int"},
    {"reg_name": "s8", "bitsize": 64, "type": "int"},
    {"reg_name": "s9", "bitsize": 64, "type": "int"},
    {"reg_name": "s10", "bitsize": 64, "type": "int"},
    {"reg_name": "s11", "bitsize": 64, "type": "int"},
    {"reg_name": "t3", "bitsize": 64, "type": "int"},
    {"reg_name": "t4", "bitsize": 64, "type": "int"},
    {"reg_name": "t5", "bitsize": 64, "type": "int"},
    {"reg_name": "t6", "bitsize": 64, "type": "int"},
    {"reg_name": "pc", "bitsize": 64, "type": "code_ptr"}
]


def rv64_parse_regs(data):
    global regs
    infos = []
    padding = 0
    p = padding
    for reg in rv64_regs:
        sz = (reg["bitsize"] >> 3) * 2
        name = reg["reg_name"]
        # print(data[p:p+sz])
        value = int(swab64(data[p:p + sz]), 16)
        p = p + sz

        infos.append((sz, name, value))
        # print(f"{name} : {hex(value)}")
    return infos


rv64_callback = {
    "s": lambda x: x.startswith("T") or x.startswith("S"),
    "g": lambda x: len(x) > 0x30,
}

"""
END
"""


class Qemu:
    def __init__(self, arch="rv64", binary="", host="127.0.0.1", port=1234):
        if arch == "rv64":
            self.regs = rv64_regs
            self.parser_regs = rv64_parse_regs
            self.callback = rv64_callback
            self.qemu = "qemu-riscv64-static"
        else:
            logging.error("TODO")
            exit(0)
        self.port = port
        self.host = host
        s = socket.socket()
        host = socket.gethostname()
        port = 1234
        if binary:
            self.binary = binary
            os.system(f"{self.qemu} -g 1234 {self.binary} &")
            sleep(1)
        s.connect((host, port))
        self.socket = s

        self.ack = ""
        self.comm("?")

    def comm(self, cmd):
        res = None
        while (1):
            self.socket.sendall(self.packet(cmd))
            res = self.socket.recv(0x1000).decode("utf-8")
            if res == "+":
                sleep(0.1)
                res = self.socket.recv(0x1000).decode("utf-8")
            # print("<--\t" + res)
            data = self.unpack(res)
            if cmd in self.callback and not self.callback[cmd](data):
                continue
            if res:
                self.ack = "+"
            else:
                self.ack = "-"
            break
        return self.unpack(res)

    def ia(self):
        while 1:
            cmd = input("> ")
            if (cmd == "exit"):
                exit(0)
            req = self.comm(cmd)

    def checksum(self, cmd):
        sum = 0
        for c in cmd:
            sum += ord(c)
        return hex(sum % 256)[2:]

    def packet(self, cmd):
        data = self.ack + "$" + cmd + "#" + self.checksum(cmd)
        # print("-->\t" + data)
        return data.encode("utf-8")

    def unpack(self, data):
        if len(data) < 4 and data != '+':
            print("reciew error data !")
            exit(-1)
        start = data.find("$")
        return data[start + 1:-3]

    def step(self):
        return self.stepn(1)

    def stepn(self, n):
        for i in range(n):
            req = self.comm("s")
        req = self.comm("g")
        return self.parser_regs(req)




if __name__ == "__main__":
    q = Qemu("rv64", "/tmp/favourite_architecture/share/main")
    t1 = time()
    for i in range(100):
        regs = q.step()
    pprint(regs)
    t2 = time()
    print("t2 - t1 " + str(t2 - t1))
