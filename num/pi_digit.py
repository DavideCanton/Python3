__author__ = 'davide'

from functools import lru_cache

PATH = r"D:\pi.txt"
A = ord('a')


@lru_cache()
def int_to_chr(i):
    return chr((int(i) % 26) + A)


if __name__ == "__main__":
    with open(PATH) as f:
        l = []
        while True:
            x = f.read(2)
            if x == "":
                break
            l.append(int_to_chr(x))
        l = "".join(l)

    print(l)

    s = input("String to search>")
    ls = len(s)
    for i in range(len(l)):
        if l[i:i + ls] == s:
            print(i)

