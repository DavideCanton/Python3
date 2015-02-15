__author__ = 'davide'

import os

PATH = "C:/Users/davide/Documents/The Witcher/saves"

if __name__ == "__main__":
    os.chdir(PATH)
    l = os.listdir()
    l.sort(key=os.path.getctime)
    for f in l[:-1]:
        os.remove(f)
        print(f, "rimosso!")
