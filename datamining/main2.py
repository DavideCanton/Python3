__author__ = 'davide'
import os
import shutil

if __name__ == "__main__":
    for i in range(10):
        os.mkdir(r"img\{}".format(i))
    with open("semeion2.arff") as f:
        src_f = r"img\{}.png"
        dst_f = r"img\{}\{}.png"
        for index, line in enumerate(f):
            if index >= 262:
                l = line.strip().split(", ")
                v = l[-1]
                i = index - 262
                shutil.move(src_f.format(i), dst_f.format(v, i))