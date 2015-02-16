import matplotlib.pyplot as plt
import numpy as np


def ch_nodes(a, b, n):
    def wrapper(i):
        return (a + b) / 2 + (b - a) / 2 * np.cos((2 * i - 1) / (2 * n) * np.pi)

    return wrapper


def main():
    a = -5
    b = 5
    n = 7
    pol_deg = 6
    x = np.r_[a:b:1000j]
    f = np.frompyfunc(lambda xx: 1 / (25 * xx ** 2 + 1), 1, 1)
    sample_x = np.r_[a:b:n * 1j]
    ch_nodes_func = ch_nodes(a, b, n)
    sample_x_ch = np.fromiter(map(ch_nodes_func, range(1, n + 1)),
                              dtype=np.float)

    plt.suptitle("$f(x) = 1/(1+25x^2)$", fontsize=20)

    # polynomials
    pol = np.polyfit(sample_x, f(sample_x), pol_deg)
    p = np.poly1d(pol)
    polc = np.polyfit(sample_x_ch, f(sample_x_ch), pol_deg)
    pc = np.poly1d(polc)

    plt.plot(sample_x, f(sample_x), "o", label="Nodi")
    plt.plot(sample_x_ch, f(sample_x_ch), "^", label="Nodi CH")
    plt.plot(x, f(x), "r-", label="f(x)")
    plt.plot(x, p(x), "b-", label="pol {} grado".format(pol_deg))
    plt.plot(x, pc(x), "g-", label="pol {} grado CH".format(pol_deg))
    plt.legend(loc=0)

    plt.figure(1).canvas.set_window_title("Fenomeno di Runge")
    plt.show()


if __name__ == "__main__":
    main()