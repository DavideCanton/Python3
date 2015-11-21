__author__ = 'Kami'

from scipy import signal
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    sys = signal.lti([1], [-1, 2], 1)
    print(sys.num)
    print(sys.den)

    # w, mag, phase = sys.bode()
    w, fr1 = sys.freqresp()
    fr, fc = np.real(fr1), np.imag(fr1)
    plt.figure(1)
    plt.subplot(211)
    plt.semilogx(w, fr)
    plt.subplot(212)
    plt.semilogx(w, fc)
    plt.show()

    print(sys.A)
    print(sys.B)
    print(sys.C)
    print(sys.D)