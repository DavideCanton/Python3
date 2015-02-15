__author__ = 'Kami'

import cmath
import matplotlib.pyplot as pl
from mpl_toolkits.axes_grid.axislines import SubplotZero


def roots_of(num, degree, polar=False):
    """
    @param num: the number
    @type num: complex
    @param degree: the degree
    @type degree: float
    @param polar: True if the number is already in polar form, False (default) else.
    @type polar: bool
    @return: The list of the roots of num.
    @rtype: [complex]
    """
    if degree <= 0:
        raise ValueError("Invalid degree")
    if not polar:
        modulo, phase = cmath.polar(num)
    else:
        modulo, phase = num

    modulo **= 1 / degree
    return [cmath.rect(modulo, (2 * cmath.pi * k + phase) / degree)
            for k in range(degree)]


if __name__ == "__main__":
    z = 2
    cs = [(round(x.real, 4), round(x.imag, 4)) for x in roots_of(z, 4)]
    x, y = zip(*cs)

    fig = pl.figure(1)
    ax = SubplotZero(fig, 111)
    fig.add_subplot(ax)

    for direction in ["xzero", "yzero"]:
        ax.axis[direction].set_axisline_style("-|>")
        ax.axis[direction].set_visible(True)

    for direction in ["left", "right", "bottom", "top"]:
        ax.axis[direction].set_visible(False)

    pl.plot(x, y, "ro")
    pl.show()