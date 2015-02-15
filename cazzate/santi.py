from urllib.request import urlopen
import re
from tkinter import Tk, Label, Button
from tkinter.constants import FALSE, N
from tkinter.font import Font
from urllib.error import URLError
from tkinter.messagebox import showerror


url = "http://www.webrun.it/Santo.asp"
# uso le lookbehind assertions
regex = r'(?<=<div align="center" class="Stile4">)[^>]*(?=</div>)'


def getSaint():
    u = urlopen(url)
    matcher = re.search(regex, u.read().decode(encoding="latin-1"))
    saints = matcher.group().split(",")
    result = []
    for saint in saints:
        s = []
        for w in saint.split():
            s.append(w[0].upper() + w[1:].lower())
        result.append(" ".join(s))
    return "\n".join(result)


class App(Tk):
    def __init__(self, master=None):
        Tk.__init__(self, master)
        self.title("Santo")
        self.resizable(FALSE, FALSE)
        self.center = Label(self, anchor=N, wraplength=300)
        self.center.configure(font=Font(size=16))
        self.button = Button(self, text="Controlla Santo",
                             command=self.controlla)
        self.button.grid(padx=80, pady=80)
        self.button.configure(font=Font(size=14))
        self.geometry("300x200")

    def controlla(self):
        try:
            s = "Oggi e'...\n\n\n" + getSaint()
            self.center.configure(text=s)
            self.button.destroy()
            self.center.grid(padx=20, pady=40)
        except URLError as e:
            showerror("Errore", "Errore: {}".format(e))

app = App()
app.mainloop()
