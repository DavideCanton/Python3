__author__ = 'Kami'

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def animate(func, w, h, step=10):
    def _animate_bars(rects):
        def wrapper(x):
            for rect, v in zip(rects, x):
                rect.set_height(v)
            return rects

        return wrapper

    fig = plt.figure()
    ax = fig.add_subplot(111)
    rects = ax.bar(range(w), np.zeros(w))
    ax.set_ylim(0, h)
    ax.set_xlim(0, w)
    ani = animation.FuncAnimation(fig, _animate_bars(rects), func, blit=False,
                                  interval=step, repeat=False)
    return plt, ani
