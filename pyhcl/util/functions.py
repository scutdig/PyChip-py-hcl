import os
import sys
import logging

class SrcInfo:
    def __init__(self, path):
        with open(path, "r") as f:
            self.lines = f.readlines()

    def getline(self, no):
        if no < len(self.lines):
            return self.lines[no].strip()
        else:
            return ""


src = None

def with_debug_info(path):
    global src
    src = SrcInfo(path)


def make_dirs(filename):
    dirname = os.path.dirname(filename)
    if dirname and not os.path.exists(dirname):
        os.makedirs(dirname, exist_ok=True)

def debug_info(depth):
    if src:
        lineno = sys._getframe(depth).f_lineno
        return f"Module {sys._getframe(depth).f_code.co_name}:{lineno}    " + src.getline(lineno-1)
    return ""