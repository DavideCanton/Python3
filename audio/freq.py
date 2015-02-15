import numpy as np
import struct
import wave
from winsound import PlaySound, SND_FILENAME, SND_ASYNC
import matplotlib.pyplot as plt

CHUNK = 1 << 8


def play(filename):
    PlaySound(filename, SND_FILENAME | SND_ASYNC)

fn = r"D:\b.wav"
f = wave.open(fn)
print(f.getparams())
ch = f.getnchannels()
sw = f.getsampwidth()
n = f.getnframes()
data = bytearray()

while len(data) < n * ch * sw:
    data.extend(f.readframes(CHUNK))

data = np.array(struct.unpack('{n}h'.format(n=n * ch), data))

w = np.fft.fft(data)
freqs = np.fft.fftfreq(len(w))
module = np.abs(w)
idmax = module.argmax()
print(abs(freqs[idmax]) * f.getframerate())

plt.specgram(data)
plt.show()
