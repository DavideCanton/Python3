from urllib.request import *
from xml.etree import ElementTree
from xml.sax.saxutils import unescape
from tkinter import tix
from tkinter import messagebox
from tkinter.constants import BOTH, END, TRUE
import webbrowser

address = "http://www.piratestreaming.net/feed_serietv.php"


def find(address):
    data = urlopen(address).read().decode()
    data = data.replace("&", "&amp;")
    document = ElementTree.XML(data)
    for el in document.findall("channel/item"):
        yield unescape(el.find("title").text), unescape(el.find("link").text)


class GUI(tix.Tk):
    def __init__(self, master=None):
        tix.Tk.__init__(self, master)
        self.geometry("500x300")
        self.title("RSS PirateStreaming")
        self.button = tix.Button(self, command=self.refresh,
                                 text="Refresh Links")
        self.button.pack(expand=TRUE)
        self.listbox = tix.Listbox(self)
        self.listbox.pack(fill=BOTH, expand=TRUE)
        self.go = tix.Button(self, command=self.go, text="Go!")
        self.go.pack(expand=TRUE)
        self.links = {}

    def refresh(self):
        self.listbox.delete(0, END)
        try:
            for name, link in find(address):
                self.links[name] = link
                self.listbox.insert(END, name)
        except Exception as e:
            messagebox.showerror("Errore", str(e))

    def go(self):
        selectedIndex = self.listbox.curselection()
        if not selectedIndex:
            return
        selectedLink = self.listbox.get(selectedIndex[0])
        webbrowser.open_new_tab(self.links[selectedLink])


if __name__ == '__main__':
    GUI().mainloop()
