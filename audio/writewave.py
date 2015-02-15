__author__ = 'davide'

from math import pi
from winsound import Beep
import wave
import numpy as np


def generateSignalStereo(sec, freq_l, freq_r, fs):
    v = generateSignal2(sec, freq_l, freq_r, fs)
    return np.asarray(v * 127 + 128, dtype=np.uint8)


def generateSignal(sec, freq, fs):
    v = np.sin(2 * pi * freq * np.arange(0, fs * sec, dtype=np.float) / fs)
    return v


def generateSignal2(sec, freq_l, freq_r, fs):
    v = np.repeat(np.arange(0, fs * sec, dtype=np.float), 2)
    v[::2] = np.sin(2 * pi * freq_l * v[::2] / fs)
    v[1::2] = np.sin(2 * pi * freq_r * v[1::2] / fs)
    return v


def generateSignalMono(sec, freq, fs):
    v = generateSignal(sec, freq, fs)
    return np.asarray(v * 127 + 128, dtype=np.uint8)


def generateScale(fs):
    w = fs
    v = np.zeros(w * 13)
    freqs = range(-9, 4)
    for i, f in zip(range(0, 13 * w, w), freqs):
        f = 440 * 2 ** (f / 12)
        for a in range(1, 5):
            v[i:i + w] += 1 / abs(a) * generateSignal(1, f * a, fs)
    return np.asarray(v * 127 + 128, dtype=np.uint8)


def generateScaleS(fs):
    w = fs * 2
    v = np.zeros(w * 8)
    freqs = [-9, -7, -5, -4, -2, 0, 2, 3]
    for i, f in zip(range(0, 8 * w, w), freqs):
        f = 440 * 2 ** (f / 12)
        for a in range(1, 2):
            v[i:i + w] += 1 / abs(a) * generateSignal2(1, f * a, f * a, fs)
    return np.asarray(v * 127 + 128, dtype=np.uint8)


if __name__ == "__main__":
    SEC = 8
    # FREQ_L = 440
    # FREQ_R = 100
    FS = 44100

    s = r"D:\prova.wav"
    f = wave.open(s, mode='wb')
    f.setnchannels(2)
    f.setsampwidth(1)
    f.setframerate(FS)

    v = generateScaleS(FS)
    it = iter(v)
    while True:
        try:
            t = [next(it), next(it)]
            # t = [next(it)]
            f.writeframes(bytes(t))
        except StopIteration:
            break
    f.close()
    Beep(100, 1000)