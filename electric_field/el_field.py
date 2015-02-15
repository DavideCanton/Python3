from tkinter import Canvas, Tk
from tkinter.constants import FALSE, LAST
import numpy as np
from numpy.linalg import norm
from tkinter.simpledialog import askfloat
from tkinter.messagebox import showinfo

WIDTH = 800
HEIGHT = 600
#RADIUS = 10
K = 9E9
INCR = 50
NORM = 20


def getVector(point, charges, normalize=True):
    E = np.zeros(2)
    for charge_point, intensity in charges.items():
        distance = point - np.array(charge_point)
        coeff = K * intensity / norm(distance) ** 3
        E += coeff * distance
    if normalize:
        E /= norm(E)
        return E * NORM + point
    else:
        return E


def get_radius(intensity):
    return 5 * np.log(abs(intensity) + 1)


class App(Tk):
    def __init__(self, master=None):
        Tk.__init__(self, master)
        self.title("Electric field")
        self.charges = {}
        self.geometry("{}x{}+200+100".format(WIDTH, HEIGHT))
        self.resizable(FALSE, FALSE)
        self.bind("<Button-1>", self.click)
        self.bind("<Button-2>", self.info)
        self.bind("<Button-3>", self.click)
        self.bind("d", self.deleteAll)
        self.canvas = Canvas(self, width=WIDTH, height=HEIGHT)
        self.canvas.pack()

    def info(self, event=None):
        if event:
            position = np.array([event.x, event.y])
            E = getVector(position, self.charges, normalize=False)
            position = np.around(position, 2)
            E = np.around(E, 2)
            msg = "Electric Field Value in {}:\nVector = {}\nModulo = {:1.4f}"
            intensity = round(norm(E), 2)
            msg = msg.format(position, E, intensity)
            showinfo("Electric Field Value", msg)

    def click(self, event=None):
        if event:
            point = event.x, event.y
            closest_point = self.find_closest(point)
            if not closest_point:
                d = 5. * (-1 if event.num == 3 else 1)
                intensity = askfloat("Value", "Charge Intensity:",
                                     initialvalue=d, parent=self)
                if intensity != 0:
                    self._insertCharge(point, intensity)

    def find_closest(self, target):
        target_array = np.array(target)
        for point, intensity in self.charges.items():
            distance = norm(np.array(point) - target_array)
            if distance < get_radius(intensity):
                return point

    def drawCircle(self, point, color, intensity, tags="circle"):
        radius = get_radius(intensity)
        top_left = [point[i] - radius for i in (0, 1)]
        bottom_right = [point[i] + radius for i in (0, 1)]
        coordinates = top_left + bottom_right
        self.canvas.create_oval(*coordinates, fill=color, tags=tags)

    def deleteAll(self, event=None):
        if event:
            self.charges.clear()
        self.canvas.delete("all")

    def _insertCharge(self, point, intensity):
        self.charges[point] = intensity
        self.deleteAll()
        for charge_point, intensity in self.charges.items():
            color = 'red' if intensity > 0 else 'blue'
            self.drawCircle(charge_point, color, intensity)
        for y in range(0, HEIGHT, INCR):
            for x in range(0, WIDTH, INCR):
                point = x, y
                E = getVector(point, self.charges)
                coordinates = point + tuple(E)
                self.canvas.create_line(*coordinates, arrow=LAST)


if __name__ == '__main__':
    App().mainloop()
