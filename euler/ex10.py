from euler._utils import genera_primi

__author__ = 'Kami'

if __name__ == "__main__":
    limit = 2E6
    s = 0
    for prime in genera_primi():
        if prime >= limit:
            break
        s += prime
    print(s)
