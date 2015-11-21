import math
import itertools as it


def caesarEncode(word, key=5):
    key %= 256
    tobytes = bytes(((c + key) % 256) for c in word.encode())
    return tobytes.decode(errors="ignore")


def caesarDecode(word, key=5):
    key %= 256
    tobytes = bytes(((c - key + 256) % 256) for c in word.encode())
    return tobytes.decode(errors="ignore")


def sqEncode(word):
    def _split(iterable, n):
        return list(zip(*[iter(iterable)] * n))

    sql = int(math.ceil(math.sqrt(len(word))))
    word += " " * (sql * sql - len(word))
    list_word = _split(word, sql)
    return ("".join(it.chain(*zip(*list_word)))).rstrip()


def main():
    while True:
        choice = input("Scelta (D/E/S)> ").upper()
        if choice == "Q":
            exit()
        elif choice == "E":
            try:
                key = int(input("Chiave (def 5)> "))
            except ValueError:
                key = 5
            word = input("Parola> ")
            print(caesarEncode(word, key))
        elif choice == "D":
            try:
                key = int(input("Chiave (def 5)> "))
            except ValueError:
                key = 5
            word = input("Parola> ")
            print(caesarDecode(word, key))
        elif choice == "S":
            word = input("Parola> ")
            print(sqEncode(word))


if __name__ == "__main__":
    print((lambda s: (lambda sq=int(math.ceil(len(s) ** 0.5)): "".join(t[1] for t in sorted(
        [((lambda q=divmod(i, sq): (q[1] * sq + q[0]))(), c) for i, c in enumerate(s + " " * (sq * sq - len(s)))])))())(input("Stringa>")))