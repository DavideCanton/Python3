__author__ = 'davide'

import wave
from random import randint, random

fs = r"D:\b.wav"
fd = r"D:\b2.wav"
L = 1 << 3
P = 1E-4

f = wave.open(fs)
f2 = wave.open(fd, "wb")
f2.setparams(f.getparams())

n = f.getnchannels()
w = f.getsampwidth()
j = 0

while True:
    p = f.readframes(L)
    if not p:
        break

    # b = bytearray(LEFT * n * w)
    b = bytearray(p)
    for i in range(L * n * w):
        if random() < P:
            b[i] = randint(0, 255)
            j += 1
    f2.writeframes(b)

print("Modificati {} bytes".format(j))
f.close()
f2.close()