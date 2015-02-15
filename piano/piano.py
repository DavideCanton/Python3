from tkinter import Tk
from tkinter.ttk import Button
from winsound import *


NOTE = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


class Player:
    def __init__(self, path):
        self.notes = {}
        with open(path) as f:
            for line in f:
                note, freq = line.split(";")
                self.notes[note] = int(freq)

    def play(self, note, duration=500):
        Beep(self.notes[note], duration)


class GUI(Tk):
    def __init__(self, player, master=None, title="Piano"):
        super(GUI, self).__init__(master)
        self.title(title)
        self.player = player
        for i in range(2, 8):
            for j in range(12):
                t = "{}{}".format(NOTE[j], i)
                b = Button(self, text=t)
                b.data = t
                b.bind('<Button-1>', self.play)
                b.grid(row=(i - 2), column=j)

    def play(self, e):
        self.player.play(e.widget.data)

player = Player("piano.txt")
app = GUI(player)
app.mainloop()
