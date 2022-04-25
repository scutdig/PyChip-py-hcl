# -*- coding: utf-8 -*-
import os
bdir = '..'
bname = " ".join(os.listdir(bdir))    # .sv/bbox/文件夹包含的文件或文件夹的名字的列表
print(bname)
x = "cp {}* ./simulation/".format(bname)
print(x)