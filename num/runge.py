import matplotlib.pyplot as plt
import numpy as np


def ch_node(a, b, i, n):
    return (a + b) / 2 + (b - a) / 2 * np.cos((2 * i - 1) / (2 * n) * np.pi)


a = -5
b = 5
n = 7
pol_deg = 6
x = np.r_[a:b:1000j]
f = np.frompyfunc(lambda x: 1 / (25 * x ** 2 + 1), 1, 1)
sample_x = np.r_[a:b:n * 1j]
sample_x_ch = np.array([ch_node(a, b, i, n) for i in range(1, n + 1)])
n = len(sample_x)

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
