import urllib.request as urlreq
import urllib.parse as parse
from PIL import Image as PILImage
from PIL import ImageTk
from tkinter import Tk, Entry, Label
from tkinter.constants import E, W, N, S, END
from tkinter.messagebox import showerror
from io import BytesIO


SIZE = 300, 300
URL_BASE = "http://chart.apis.google.com/chart"
DATA = {"cht": "qr", "chs": "x".join(str(c) for c in SIZE), "chld": "H|0"}


class MyFrame(Tk):
    def __init__(self, master=None):
        Tk.__init__(self, master)

        self.title("Prova QR")
        self.center(SIZE[0], int(SIZE[1] * 1.1))

        Label(self, text="Stringa:").grid(row=0, column=0, sticky=E)
        self.input = Entry(self)
        self.input.grid(row=0, column=1, sticky=W)
        self.input.bind("<Return>", self.returnPressed)

        self.panel = Label(self)
        self.panel.grid(row=1, columnspan=2, sticky=W + E + N + S)

    def center(self, width, height):
        screen_size = self.winfo_screenwidth(), self.winfo_screenheight()
        size = [width, height]
        pos = [(screen_size[i] - size[i]) // 2 for i in (0, 1)]
        self.geometry("{}x{}+{}+{}".format(*(size + pos)))

    def returnPressed(self, _):
        DATA["chl"] = self.input.get()
        try:
            url = URL_BASE + "?" + parse.urlencode(DATA)
            connection = urlreq.urlopen(url)
        except Exception as e:
            showerror("Errore ".format(e))
        else:
            byte_io = BytesIO(connection.read())
            self.image = PILImage.open(byte_io)
            self.updatePanel()
            self.input.delete(0, END)

    def updatePanel(self):
        self.imageTK = ImageTk.PhotoImage(self.image)
        self.panel.configure(image=self.imageTK)
        self.update()


if __name__ == "__main__":
    MyFrame().mainloop()
