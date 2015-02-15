from winsound import Beep
from tkinter import Canvas, Tk
from tkinter.constants import FALSE
from math import hypot
from tkinter.messagebox import showinfo
from random import randint

WIDTH = 800
HEIGHT = 600
FREQMIN = 100
FREQMAX = 8000
RADIUS = 10
WAVES = False


def distance(p1, p2):
    return hypot(p1[0] - p2[0], p1[1] - p2[1])


DISTMAX = distance((0, 0), (WIDTH, HEIGHT))


class App(Tk):
    def __init__(self, master=None):
        Tk.__init__(self, master)
        self.title("Gioca!!!")
        self.geometry("{}x{}+200+200".format(WIDTH, HEIGHT))
        self.point = randint(0, WIDTH - 1), randint(0, HEIGHT - 1)
        self.resizable(FALSE, FALSE)
        self.bind("<Button-1>", self.click)
        self.canvas = Canvas(self, width=WIDTH, height=HEIGHT)
        self.canvas.pack()

    def click(self, event=None):
        if event:
            point = event.x, event.y
            dist = distance(point, self.point)
            rel = 1 - dist / DISTMAX
            color = self._color(rel)

            self.drawCircle(point, color)
            if WAVES:
                self.drawWave(point, color)

            if dist <= 5:
                self.unbind_all("<Button-1>")
                showinfo(title="Trovato", message="Trovato!!!")
                self.destroy()
            else:
                self.beepAtFreq(rel)

    @staticmethod
    def _color(rel):
        if rel <= 0.5:
            return "red"
        elif 0.5 <= rel <= 0.9:
            return "yellow"
        else:
            return "green"

    def drawWave(self, point, color):
        center = self.point
        radius = distance(center, point)
        p1, p2 = self._circle(self.point, radius)
        self.canvas.create_oval(*(p1 + p2), outline=color, tags="wave")

    @staticmethod
    def beepAtFreq(rel):
        freq = int(rel * (FREQMAX - FREQMIN)) + FREQMIN
        Beep(freq, 300)

    def drawCircle(self, point, color):
        self.canvas.delete("circle")  # rimuove i cerchi
        p1, p2 = self._circle(point, RADIUS)
        self.canvas.create_oval(*(p1 + p2), fill=color, tags="circle")

    @staticmethod
    def _circle(point, radius):
        p1 = [point[i] - radius for i in (0, 1)]
        p2 = [point[i] + radius for i in (0, 1)]
        return p1, p2


if __name__ == '__main__':
    App().mainloop()
