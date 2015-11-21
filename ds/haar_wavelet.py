__author__ = 'davide'

import numpy as np


class HaarWavelet:
    def __init__(self, signal):
        signal_length = len(signal)
        if signal_length and signal_length & (signal_length - 1):
            # if len(signal) is not a power of 2
            raise ValueError()
        array = signal
        result = np.zeros_like(array)
        while len(array) > 1:
            averages = (array[::2] + array[1::2]) / 2.0
            averages_length = signal_length // 2
            start = signal_length - averages_length
            end = signal_length
            result[start:end] = array[::2] - averages
            signal_length -= averages_length
            array = averages
        result[0] = array[0]
        self.signal = result

    def __getitem__(self, item):
        lower = 0
        upper = self.signal.shape[0] - 1
        position = 1
        value = self.signal[0]
        while lower < upper:
            middle = (lower + upper) // 2
            if item <= middle:
                value += self.signal[position]
                position *= 2
                upper = middle
            else:
                value -= self.signal[position]
                position = 2 * position + 1
                lower = middle + 1
        return value


def cumsum(f):
    c = np.cumsum(f, dtype=np.float)
    l = len(c)
    if l and l & (l - 1):
        x = 1 << (l.bit_length())
        return np.concatenate([c, [c[-1]] * (x - l)])
    else:
        return c


if __name__ == "__main__":
    s = np.array(np.random.random_integers(0, 10, 8), dtype=np.uint8)
    f = np.bincount(s)
    c = cumsum(f)
    w = HaarWavelet(c)
    print(s)
    print(w.signal)
    d = np.array([w[i] for i in range(len(c))])
    print(d)
    print(np.array_equal(d, c))
